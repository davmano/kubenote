# Use a lightweight Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

# Set environment and port
ENV PORT=5000
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]

