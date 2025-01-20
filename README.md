# User Profile Audit System  

![coverage.svg](static/coverage.svg)

## **Overview**  
The **User Profile Audit System** is a backend application designed to manage user profiles and ensure no data is permanently lost. All changes, deletions, and updates to user profiles are logged and auditable, with the ability to restore user profiles to a previous state.  

This project is built using Python's **FastAPI**, PostgreSQL, and follows the **Zen of Python** principles for elegant and simple design.  

---

## **Features**  
- **Swagger API Documentation**
- **User CRUD Operations**: Create, Read, Update, and Delete user profiles.  
- **Audit Logging**: Tracks all changes to user profiles.  
- **Point-in-Time Restoration**: Restore a user profile to a specific historical state.  
- **Authentication**: Secure endpoints using Basic Authentication.  
- **Best Practices**: RESTful API design, validations, and error handling.  
- **Kubernetes Deployment**: Configurations for deployment in a Kubernetes environment.  

---

## **Project Structure**  
The project follows a layered architecture for scalability and maintainability:  

    user-profile-audit/
        ├── app/
        │ ├── db/ # Database operations and migrations 
        │ ├── models/ # Pydantic models for validation
        │ └── main.py # Application entry point and endpoint managment
        ├── tests/ # Test suite 
        ├── Dockerfile # Docker configuration 
        ├── kubernetes/ # Kubernetes manifests 
        ├── .env # Environment variables 
        ├── README.md # Project documentation 
        └── requirements.txt # Python dependencies


---

## **Setup Instructions**  
### **Prerequisites**  
- Python 3.12 or higher  
- PostgreSQL  
- Docker (optional, for containerized setup)  

### **Installation**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/chmbrs/user-profile-audit.git
   cd user-profile-audit
   ```

    1.1 (Optional recommended) 
    Use a virtual environment to manage python dependencies.

    ```bash
     python3 -m venv .venv
     source .venv/bin/activate
    ```


2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
   
   or using pip-tool:
   ```bash
   pip install pip-tool
   pip-sync requirements.txt dev-requirements.txt
   ```

3. Set up environment variables in a .env file:
```dotenv
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/user_audit
SECRET_KEY=<your_secret_key>
```

4. Initialize the database:
    ```bash
    python scripts/initialize_db.py
    ```
---

## **Usage**  

### **Run the Application**

```bash
uvicorn app.main:app --reload --env-file .env
```

**DOCUMENTATION:** http://localhost/docs

### **Endpoints**

1. User CRUD Operations

- `POST /users`: Create a new user.

- `GET /users/{id}`: Get a user.

- `GET /users`: List all users.

- `PUT /users/{id}`: Update a user.

- `DELETE /users/{id}`: Delete a user.

2. Audit Logs

- `GET /audit`: View all changes to user profiles.

3. Restore User

- `POST /restore/{id}`: Restore a user to a specific point in time.

## **Testing**
Run tests using pytest:

```bash
pytest --cov=app
```

## **Deployment**
### **Docker**

1. Build and run the Docker container:
    ```bash
    docker build -t user-profile-audit .  
    docker run -p 8000:8000 --env-file .env user-profile-audit  
    ```

### **Kubernetes**
1. Apply Kubernetes manifests:
    ```bash
    kubectl apply -f kubernetes/
    ```
---
## **Development Roadmap**

### **Milestone 1: Project Setup**
Folder structure and initialize project.
Git flow init.

### **Milestone 2: CRUD Operations**
User CRUD endpoints with SQL-based operations.

### **Milestone 3: Audit Logging and Restoration**
Audit logging and point-in-time restoration.

### **Milestone 4: Authentication and Deployment**
Secure endpoints with Basic Authentication and prepare Kubernetes configurations.


### **Time Taken**
Milestone 1 = 1 hour
Milestone 2 = 3 hours
Milestone 3 = 2.5 hour

#### **Contact**
For any questions, reach out to juanjosechambers@gmail.com