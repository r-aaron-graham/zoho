# CRM Contact Integration Example

A local mapping example for CRM contact exports using Zoho-style field names. The repository began empty. This implementation uses synthetic records to demonstrate validation, normalization, and duplicate detection.

## Run

Python 3.12 and the standard library are sufficient.

```sh
python contacts.py
python -m unittest -v
```

The demo prints one normalized record with external_id, last_name, and email. No credentials are required.

## Contract

Call normalize_batch with a list of dictionaries. Each record requires nonempty string id and Last_Name fields. Email is optional and accepts nonempty text or null. IDs and names are trimmed. Duplicate IDs after trimming reject the batch. The function validates all records before returning results and performs no external writes.

## Integration scope

This is an offline transformation example. Live Zoho API compatibility, OAuth, pagination, API quotas, persistence, retries, and email-address syntax validation require further implementation and verification. The sample contains fictional data. Extend the contract against the actual export or API schema before connecting an account.

## File conversion and installation

Run `python contacts.py --input contacts.json --output normalized.json`. Invalid input exits with code 2 and preserves existing output. Valid batches replace output atomically using a temporary file in the destination directory. The destination directory must already exist.

Install with `python -m pip install .`, then run `crm-normalize`. The container workflow installs the package, scans application code with Bandit, builds the image, and runs the tests without network access. Build locally with `docker build -t crm-mapping .`.
