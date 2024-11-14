# Python image base
FROM python:3.12

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="$HOME/.local/bin:$PATH" && \
    poetry config virtualenvs.create false  # Install dependencies globally in the container environment

# Copy only the necessary files for dependency installation
COPY ./pyproject.toml ./poetry.lock* /app/

# Set the working directory
WORKDIR /app

# Install dependencies using Poetry
RUN /root/.local/bin/poetry install --no-root --no-interaction --no-ansi

# Copy data
COPY . /app

# Run Script
# Ensure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
