# Use Python as base image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install git
RUN apt-get update && apt-get install -y git && apt-get clean

# Set working directory inside the container
WORKDIR /app

# Clone the repository
RUN git clone https://github.com/Xenoth/pyminitel.git repo && \
    cd repo && \
    python3 -m pip install .

# Set the working directory to the cloned repository
WORKDIR /app/repo

# Run the script as CMD
CMD ["python3", "src/examples/xenas.py"]