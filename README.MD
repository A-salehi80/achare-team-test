Django Authentication System with Phone Number Verification

This project is a Django-based authentication system that uses phone number verification. It leverages Celery and Redis or RabbitMQ for sending SMS to avoid server load, and SQLite for a simple, file-based database.
Features

    Phone Number Authentication: Users can authenticate using their phone numbers.
    Verification Codes: Verification codes are sent via SMS (displayed in the console for testing).
    Middleware for Security: Middleware to track wrong credentials and manage failed verification attempts.
    Custom Superuser Command: Modified createsuperuser command to include phone number authentication.

Getting Started
Prerequisites

    Python 3.x
    Django
    Django REST Framework

Installation

    Clone the repository:



git clone https://github.com/A-salehi80/achare-team-test
cd achare_test

Install dependencies:



pip install -r requirements.txt

Apply migrations:



python manage.py migrate

Create superuser:



    python manage.py createsuperuser --phone 09120573396 --password aa1234

Running the Application

    Start the development server:



    python manage.py runserver

    Access the application at http://127.0.0.1:8000/.

Testing

Superuser Credentials

    Phone Number: 09120573396
    Password: aa1234


Verification Codes

Verification codes are displayed in the console for easy testing.


Code Style

The codebase is PEP8 friendly and includes comments for better understanding.


Middleware

Custom middleware is implemented to track wrong credentials and handle three failed verification attempts.

_______________________________________________________________________________________
for Achare Team: tnx for giving me this chance

I used SQLite because I wanted easier configuration, so it's easier for you to test it,otherwise using POSTGRESS as DATABASE is prefered.

For sending SMS, it's better to use queuing with Celery and Redis or RabbitMQ to avoid imposing load on the server.

For tracking wrong credentials and three failed verification attempts blocking, I made middleware.

I changed the createsuperuser command, so I could create a superuser with a phone number.

Verification codes are shown in the console, making it easy to test verification .I had to override authentication.

The code is fully PEP8 friendly, and I have added some comments that may help to make the code more understandable.