# Pull base image of Python 3.9 from Docker Officail Images
FROM python:3.9

# Add backend directory to make absolute filepaths consistent across services
WORKDIR /app_backend

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --upgrade pip -r requirements.txt

# Copies everything over to the Docker environment
COPY . .

# Make port 8000 available for the app
EXPOSE 8000

# Start app
CMD python3 manage.py runserver 0.0.0.0:8000
