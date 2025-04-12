FROM python:3.12.7-slim

RUN mkdir -p /home/app

WORKDIR /home/app

COPY . /home/app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]