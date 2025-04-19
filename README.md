# VidStream
VidStream is a video streaming platform built with Django and PostgreSQL. It enables users to sign in, upload videos, and watch content shared by others. The platform supports essential features like user authentication and video management to provide a smooth content-sharing experience.

## Features
- User authentication (Sign In, Sign Up, Sign Out).
- Video upload and streaming.
- Video gallery to browse through uploaded content.
- Basic contact functionality for users to reach out.

## Usage:
### Basic setup and dependency management:
- Install `pipenv`:
```bash
pip install pipenv
```

- Activate the Virtual Environment:
```bash
pipenv shell
```

- Install required libraries from the `Pipfile.lock`:
```bash
pipenv install
```

OR

- Using pre-installed "venv" to create Virtual Environment:
```bash
python -m venv .venv
```

- Activate the Virtual Environment:
```bash
.venv/Scripts/activate.ps1
```

- Install all requirements from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Pre-requisites:
- Updations Required in .env file for auth, db,etc.

- Migrations, since we are using postgres, to create all tables in db:
```bash
python manage.py migrate
```

### To run the code:
- Run the server with:
```bash
python manage.py runserver
```

- Access the application at `http://127.0.0.1:8000/` in your browser.

## Description about various files:
- **manage.py**: The Django project management command-line utility.
- **VidStream**:
    - **settings.py**: Contains settings and configuration for the Django project.
    - **urls.py**: The URL configuration for the project, mapping URLs to views.
    - **wsgi.py**: Helps to serve the Django application in production.
    - **asgi.py**: Used to serve the application in an ASGI-compatible server.

- **Home app**:
  - **views.py**: Handles the logic for views like sign-in, sign-up, login, and contact.
  - **urls.py**: Maps the URLs related to user authentication to views.

- **Stream app**:
  - **views.py**: Manages video upload, display in the gallery, and related content functionality.
  - **urls.py**: Defines URLs for video-related features (upload, gallery).

- **templates**: Contains HTML files for the whole project in a systematic file structure.
- **media**: The folder where uploaded videos are stored.
- **Pipfile**: Defines the dependencies used in the project.
- **Pipfile.lock**: Locks the dependencies to a specific version for consistency across environments.
- **requirements.txt**: Defines the dependencies used in the project