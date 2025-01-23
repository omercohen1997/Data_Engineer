FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .
COPY templates templates/

# Expose the port the app runs on
EXPOSE 5000

# Define environment variable
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["flask", "run"]

