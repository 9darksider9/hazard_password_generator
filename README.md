# 🔐 Password & Passphrase Generator

This project provides a **secure password and passphrase generator** with:
- A **FastAPI backend** for API-based password/passphrase generation
- A **Streamlit frontend** for easy user interaction
- **Dockerized deployment** for simple setup and usage

---

# **🚀 Features**
✅ Generate **random secure passwords**  
✅ Generate **random passphrases** using the **EFF Diceware wordlist**  
✅ **No authentication required** for API and Streamlit app  
✅ **Lightweight & fast deployment** via Docker  

---

## **📌 Setup & Installation**

### **1️⃣ Prerequisites**
Ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Navigate to the directory `password-generator` and run the following:
    * ```docker-compose build```
    * ```docker-compose up -d```

---

## **📄Access the Application**
- Streamlit App: http://localhost:8501
- FastAPI Docs: http://localhost:8000/docs
    * ```curl -X GET "http://localhost:8000/docs"```
- FastAPI OpenAPI JSON: http://localhost:8000/openapi.json
    * ```curl -X GET "http://localhost:8000/openapi.json"```

---

## **🔌API Call Examples**

- Ensure all is up and running
    * API Endpoint - GET /health
    * Example Call
        ```
        curl -X GET "http://localhost:8000/health"
        ```
    * Example Response
        ```
        {"status": "ok", "database": "reachable"}
        ```

- Generate Password Example Call
    * API Endpoint - POST /generate_password
    * Parameters
        ```
        {
            "length": 12,
            "use_uppercase": true,
            "use_lowercase": true,
            "use_numbers": true,
            "use_specials": true
        }
        ```
    * Example Call
        ```
        curl -X POST "http://localhost:8000/generate_password" \
            -H "Content-Type: application/json" \
            -d '{"length": 12, "use_uppercase": true, "use_lowercase": true, "use_numbers": true, "use_specials": true}'
        ```
    * Example Response
        ```
        {"password": "aX9$e!KqP0wz"}
        ```

- Generate Passphrase Example Call
* API Endpoint - POST /generate_passphrase
    * Parameters
        ```
        {
            "num_words": 4
        }
        ```
    * Example Call
        ```
        curl -X POST "http://localhost:8000/generate_passphrase" \
            -H "Content-Type: application/json" \
            -d '{"num_words": 4}'
        ```
    * Example Response
        ```
        {"passphrase": "correcthorsebatterystaple"}
        ```
