FROM python:slim

WORKDIR /taskapi

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "${APP_PORT:-8000}"]
