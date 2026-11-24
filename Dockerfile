FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY main.py errors.py test_errors.py test_main.py ./
COPY raw_data/property_data_raw.csv ./raw_data/

ENTRYPOINT ["python", "main.py"]
CMD ["raw_data/property_data_raw.csv"]
