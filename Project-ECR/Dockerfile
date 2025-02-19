# Use the official Python image as the base
FROM python:latest

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy   

COPY . .

# Expose the port on which the app will run
EXPOSE 8000

# Command to run the app
CMD ["python", "./app.py"]
