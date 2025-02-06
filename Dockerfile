# Use the official Python image as a base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files into the container
COPY requirements.txt ./
COPY app ./app
COPY streamlit_app.py ./
COPY config.toml /root/.streamlit/config.toml

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose both FastAPI and Streamlit ports
EXPOSE 8000 8501

# Command to run both FastAPI and Streamlit in the same container
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 & \
    streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0