# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /gradinaCraciun/

ENV PYTHONPATH="/gradinaCraciun/"

COPY requirements.txt /gradinaCraciun/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /gradinaCraciun/

EXPOSE 8000

CMD ["gunicorn", "gradinaCraciun.wsgi:application", "--bind", "0.0.0.0:8000"]
