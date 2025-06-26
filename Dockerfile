# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install build tools for Rust-based packages
RUN apt-get update && apt-get install -y build-essential curl git && \
    apt-get install -y libssl-dev && \
    apt-get clean

# Install Rust (for maturin)
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
