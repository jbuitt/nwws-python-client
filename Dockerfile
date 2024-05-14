FROM python:3

# Set working directory
WORKDIR /app

# Copy required files to work directory
COPY nwws.py .
COPY requirements.txt .

# Run apt update
RUN pip install --no-cache-dir -r requirements.txt

# Run NWWS ingester
CMD ["python", "nwws.py", "config.json"]
