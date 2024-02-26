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
   
   The communication between service has a validator for IP address. If you want to test on multiple machine. Please add another IP at [app_url](url_service/app_url.py) at line 155.

   This will start a development server, by default, the url service launch at port 5000 and the authentication launch at port 5001.