# Base image: a small Python runtime (no extra packages needed,
# the app only uses Python's standard library)
FROM python:3.12-slim

# All following instructions run relative to /app inside the container
WORKDIR /app

# Copy the app's source code into the image
COPY app.py .

# Document the port the app listens on inside the container
EXPOSE 5000

# Default command run when the container starts
CMD ["python", "app.py"]