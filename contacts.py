"""Map a synthetic CRM contact export into a normalized integration record."""
import json
import argparse
import os
from pathlib import Path
import tempfile


def normalize_contact(record):
    if not isinstance(record, dict):
        raise ValueError("Contact must be an object")
    contact_id = record.get("id")
    last_name = record.get("Last_Name")
    email = record.get("Email")
    if not isinstance(contact_id, str) or not contact_id.strip():
        raise ValueError("Contact id must be nonempty text")
    if not isinstance(last_name, str) or not last_name.strip():
        raise ValueError("Last_Name must be nonempty text")
    if email is not None and (not isinstance(email, str) or not email.strip()):
        raise ValueError("Email must be nonempty text or null")
    return {"external_id": contact_id.strip(), "last_name": last_name.strip(),
            "email": email.strip() if email else None}


def normalize_batch(records):
    if not isinstance(records, list):
        raise ValueError("Expected an array of contacts")
    contacts = [normalize_contact(record) for record in records]
    ids = [contact["external_id"] for contact in contacts]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate contact IDs")
    return contacts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="JSON array of contact records")
    parser.add_argument("--output", type=Path, help="Atomically replace this JSON output")
    args = parser.parse_args()
    temporary = None
    try:
        records = json.loads(args.input.read_text(encoding="utf-8")) if args.input else [
            {"id": "example-1", "Last_Name": "Example", "Email": "example@example.invalid"}
        ]
        payload = json.dumps(normalize_batch(records), indent=2) + "\n"
        if args.output:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                             dir=args.output.parent, delete=False) as handle:
                temporary = handle.name
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, args.output)
            temporary = None
        else:
            print(payload, end="")
    except (ValueError, OSError, RecursionError) as exc:
        parser.exit(2, f"Contact conversion failed: {exc}\n")
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
