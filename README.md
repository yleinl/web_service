# URL Shortener REST API Documentation

This document provides an overview and setup guide for a REST API project designed to shorten URLs. The project is structured into five main Python files, each serving a distinct role within the application.

## Project Structure

- `app.py`: The entry point of the Flask application. It defines the Flask app and the routes for handling requests.
- `database.py`: Contains the setup for the SQLAlchemy database, including the engine and session configuration.
- `models.py`: Defines the SQLAlchemy ORM models used by the application, notably the model for shortened URLs.
- `url_service.py`: Includes the CRUD operations on database.
- `utils.py`: Provides utility functions, such as those for generating a short URL identifier, check URL format and so on.

## Setup and Installation

1. **Install Dependencies**: First, install the required Python packages by running the following command:

    ```bash
    pip install Flask SQLAlchemy requests Flask-SQLAlchemy PyMySQL mysqlclient
    ```

    Replace `mysqlclient` with the appropriate driver for your database if not using MySQL.

2. **Database Configuration**: Edit `database.py` to configure your database connection string. You will need to replace placeholders with your database credentials:

    ```python
    USERNAME = 'your_username'
    PASSWORD = 'your_password'
    HOST = 'your_host'
    PORT = '3306'
    DATABASE = 'your_database_name'
    ```

3. **Initialize the Database**: Before running the application for the first time, ensure your database is accessible and the connection parameters are correctly set. The models defined in `models.py` will be used to create the necessary tables.

4. **Run the Application**: Launch the Flask application by running `app.py`:

    ```bash
    python app.py
    ```

    This will start a development server, typically accessible at `http://127.0.0.1:5000/`.

## Using the API

With the server running, you can now use the API to shorten URLs and retrieve original URLs using the generated short identifiers. Here's how to interact with the API:

- **Shorten a URL**: Send a POST request to the root endpoint (`/`) with a JSON body containing the URL to be shortened:

    ```json
    {
      "value": "https://fastapi.tiangolo.com"
    }
    ```

    The response will include the shortened URL identifier.

- **Retrieve a URL**: Send a GET request to `/<short_id>`, where `<short_id>` is the identifier returned when the URL was shortened. The response will redirect you to the original URL.
