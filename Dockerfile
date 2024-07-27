# Use the official Python image as a base image
FROM python

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY . /app

# Install paho-mqtt library
RUN pip install paho-mqtt==1.5.1

# Command to run the Python script
CMD ["python3", "client.py"]
