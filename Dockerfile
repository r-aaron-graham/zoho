FROM python:3.12-slim
WORKDIR /app
COPY contacts.py test_contacts.py ./
USER 65534:65534
CMD ["python", "contacts.py"]
