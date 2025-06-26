# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system packages for building if needed
RUN apt-get update && apt-get install -y build-essential curl git && \
    apt-get install -y libssl-dev && apt-get clean

# Install Rust (in case any Gemini sub-dependencies trigger maturin)
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
