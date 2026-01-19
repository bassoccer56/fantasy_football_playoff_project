FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (this helps Docker cache your libraries)
COPY requirements.txt .

# Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code (like main.py)
COPY . .

CMD ["python", "main.py"]