# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port streamlit runs on
EXPOSE 8080

# Run app.py when the container launches
# CMD ["streamlit", "run", "streamlit.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS false"]
CMD streamlit run --server.port 8080 --server.enableCORS false Home.py