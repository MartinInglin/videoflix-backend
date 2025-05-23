## Project overview

This backend provides API endpoints for managing video uploads, encoding videos to multiple resolutions, tracking user watch history, and handling user registration, login / logout, email verification and password reset. It is built with Django and designed to support a video streaming platform.


## System requirements

- Linux (tested on Ubuntu 20.04 and higher)
- Python 3.8
- Redis
- FFmpeg (for media processing)

To install FFmpeg on Ubuntu:

```bash
sudo apt install ffmpeg
```


## Installation

1. Clone the repository:
   
```bash
git clone https://github.com/MartinInglin/videoflix-backend
cd videoflix-backend
```

2. Set up a virtual environment
   
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Environment variables
Create a `.env` file in the root directory and add the following environment variables:

EMAIL_HOST_PASSWORD=
DATABASE_PASSWORD=
REDIS_PASSWORD=
RQ_PASSWORD=


## Running the application

To start the development server, run:

```bash
python manage.py runserver
```

Make sure Redis is running for background tasks:

```bash
redis-server
```

To start the RQ worker for processing tasks:

```bash
python manage.py rqworker
```


## Database setup

Apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create a superuser to access the Django admin:

```bash
python manage.py createsuperuser
```


## API endpoints

- `/api/registration/` - POST - Create a new user.
- `/api/verification/` - POST - Save the verification of a user.
- `/api/resend_verifiction/` - POST - Resends a verification email.
- `/api/forgot_password/` - POST - Sends email to reset password.
- `/api/reset_password/` - POST - Resets a password.
- `/api/login/` - POST - Logs in a user.
- `/api/logout/` - POST - Logs out a user.*
- `/api/dashboard/` - GET - Gets the data for the dashboard.*
- `/api/hero/` - GET - Gets the data for the hero section.*
- `/api/video/<id>/` - GET - Gets the data for a video.*
- `/api/update_watch_history/<id>/<resolution>` - POST - Updates the watch history of a user.*

*authentication token required


## Managing videos

To add a video, run the server and open it in the browser. Click on videos / add video.

To add a new video category add it in content/models.py in the video model to the array CATEGORY_CHOICES.

Once a video has been uploaded:

    Title and Video File: These fields cannot be edited. If changes are necessary, the existing video must be deleted, and a new video should be uploaded with the updated details.
    This approach ensures consistency in video metadata and avoids complications in the system.


## Managing users

When registrating a user, please make sure that the username and email are equal. As in the front end only the email is asked during registration, the email is set as the username which then will be used for the login process.

## Running tests

Run the Django test suite with:

```bash
python manage.py test
```

To run tests with a debugger use the python debugger. Adjust launch.json to access specific tests or test groups.


## Creating requirements

Create requiremtents.txt:

```bash
pip freeze > requirements.txt
sed -i 's/^backports.zoneinfo==.*/backports.zoneinfo==0.2.1; python_version<"3.9"/' requirements.txt
```

## Docker

Start the server:
```bash
sudo docker-compose up -d
```

Stop the server:
```bash
sudo docker-compose down
```

Rebuild images:
```bash
sudo docker-compose up --build
```
or
```bash
sudo docker build -t <image_name>:latest .
```
for creating the nginx and rq-worker images you need to add the path to the Dockerfile
```bash
docker build -f rq-worker/Dockerfile -t europe-west6-docker.pkg.dev/videoflix-439014/videoflix/rq-worker-image:latest .
docker build -t europe-west6-docker.pkg.dev/videoflix-439014/videoflix/nginx-image:latest -f nginx/Dockerfile .
```

Run docker container locally:
```bash
docker-compose -f docker-compose.dev.yml up -d
```

Enter docker container:
```bash
docker excec -it <nameOrIdOfContainer> bash
```
