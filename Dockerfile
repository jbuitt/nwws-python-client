FROM ubuntu:18.04

# Set working directory
WORKDIR /app

# Copy required files to work directory
COPY nwws.py requirements.txt .

# Clean out apt cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Update package repository
RUN apt-get update 

# Run apt update
RUN apt-get install -y python3-pip

# Install Python deps
RUN pip3 install -r requirements.txt

# Run NWWS ingester
CMD ["python3","nwws.py","config.json"]

