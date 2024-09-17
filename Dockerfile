FROM python:3.11

# Set the working directory
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY data/* /app/data/
COPY src/* /app/src/
COPY app.py /app/


ENTRYPOINT [ "streamlit", "run", "app.py" ]