# URL Shortener REST API Documentation

This document provides an overview and setup guide for a REST API project designed to shorten URLs. The project is structured into five main Python files, each serving a distinct role within the application.

## Project Structure

- `auth_service`: The entry point of the Flask application. It defines the Flask app and the routes for handling requests.
- `url_service`: Includes the CRUD operations.
- `app_auth.py`: The entry point of the authentication service
- `test_auth.py`: The entry point of the url shorten service

## Setup and Installation

1. **Install Dependencies**: First, install the required Python packages by running the following command:

    ```bash
    pip install Flask requests 
    ```

2. **Run the Application**: Launch the Flask application by running `app.py`:

    ```bash
    python auth_service/app_auth.py
    python url_service/app_url.py
    ```
   For each time you test the authentication service, please delete the `user_auth.db` after testing.

    This will start a development server, by default, the url service launch at port 5000 and the authentication launch at port 5001.


### Docker vitrualization
1. **For url shorten service**
 ```bash
cd url_service
docker build -t url_service:latest .
```
2. **For authentication service**
 ```bash
cd auth_service
docker build -t auth_service:latest .
```
3. **Docker Compose**
 ```bash
In this dicrectory
docker-compose up
```
### Kubenetes Deployment
 ```bash
cd yaml
kubectl apply -f deployment.yaml
kubectl apply -f nfs-server-deploy.yaml
kubectl apply -f nfs-svc.yaml
kubectl apply -f nginx-config.yaml
kubectl apply -f nginx-deployment.yaml
kubectl apply -f nginx-service.yaml
kubectl apply -f service1.yaml
kubectl apply -f service2.yaml
```
