FROM python:3.13

WORKDIR /app

# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

 RUN pip install --upgrade pip

 COPY requirement.txt /app/

 RUN pip install --no-cache-dir -r requirement.txt

 copy . /app/

 CMD ["python","manage.py","runserver","0.0.0:8000"]
