# Use the official Python image from DockerHub
FROM python:3.12-slim

# Set environment variables to run in production mode
ENV ENV=production
# Set environment variables to prevent Python from writing pyc files and
ENV PROD_DATABASE_URI=''
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /src

# Update and upgrade the system packages (using apt for slim, which is debian based)
RUN apt-get update && apt-get upgrade -y

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . /src/

# Expose the port the app will run on (default Flask port is 5000)
# Flask default is 5000, but typically production apps use 80 or 8080
EXPOSE 8000


CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "wsgi:app"]
