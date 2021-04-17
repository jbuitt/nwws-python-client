FROM ubuntu:20.04

# Set working directory
WORKDIR /app

# Copy required files to work directory
COPY nwws.py .

# Don't prompt for questions during apt-get
ENV DEBIAN_FRONTEND noninteractive

# Clean out apt cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Update package repository
RUN apt-get update

# Run apt update
RUN apt-get install -y python3-pip python3-pyasn1 python3-pyasn1-modules python3-sleekxmpp

# Run NWWS ingester
CMD ["python3","nwws.py","config.json"]
