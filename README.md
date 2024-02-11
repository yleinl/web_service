# URL Shortener REST API Documentation

This document provides an overview and setup guide for a REST API project designed to shorten URLs. The project is structured into five main Python files, each serving a distinct role within the application.

## Project Structure

- `app.py`: The entry point of the Flask application. It defines the Flask app and the routes for handling requests.
- `url_service.py`: Includes the CRUD operations.
- `utils.py`: Provides utility functions, such as those for generating a short URL identifier, check URL format and so on.

## Setup and Installation

1. **Install Dependencies**: First, install the required Python packages by running the following command:

    ```bash
    pip install Flask SQLAlchemy requests Flask-SQLAlchemy PyMySQL mysqlclient
    ```

2. **Run the Application**: Launch the Flask application by running `app.py`:

    ```bash
    python app.py
    ```

    This will start a development server, by default, it launch at port 5000 and can be accessible at `http://127.0.0.1:5000/`.
    You can configure the port by setting at: 
    ```python
    app.run(port={port})
    ```
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
