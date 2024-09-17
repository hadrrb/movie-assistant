FROM python:3.11

# Set the working directory
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/ ./app/src

RUN python src/ingest.py


ENTRYPOINT [ "streamlit", "app.py" ]