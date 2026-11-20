"""Map a synthetic CRM contact export into a normalized integration record."""
import json


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


if __name__ == "__main__":
    print(json.dumps(normalize_batch([
        {"id": "example-1", "Last_Name": "Example", "Email": "example@example.invalid"}
    ]), indent=2))
