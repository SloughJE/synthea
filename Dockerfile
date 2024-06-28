# Use a base image with Java and Python installed
FROM openjdk:11-jdk-slim

# Install Python and other necessary tools
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of your application files
COPY . .
