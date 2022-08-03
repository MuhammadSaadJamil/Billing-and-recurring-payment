# Billing & Recurring Payment System
This application is a subscription based system that allow payment integration and recurring payments.
#### Version 1.0
## Stack
This application uses:
1. Python
2. Django
3. HTML
4. CSS
5. Bootstrap 4

## How to run application
1. Install required python packages using
```bash
pip install -r requirements.txt
```
2. Setup Database connection in settings.py. 
By default, the application uses SQLite3 but can 
detect Postgres db on heroku and add it automatically
3. Create .env file and setup env variables *( format provided below )*
4. Run migrations using
```bash
python manage.py migrate
```
5. Create admin user using
```bash
python manage.py createsuperuser 
```
6. Start server using
```bash
python manage.py runserver 
```
The application will start on **127.0.0.1:8000**

## Features
Version 1.0 of application supports
1. Creation and management of users (admin, buyer).
2. Email authentication.
3. CRUD for features.
4. CRUD for plans.
5. Profile management and update.
6. Read and Update operations for usage.
7. Transaction using stripe.
8. Adding card using stripe.
9. Automatic subscription payment using background tasks.
10. Transaction history.
11. Automatic overuse payment calculation and processing.
12. Email invoice for payments.
13. File storage on cloudinary.

## Assumptions
1. Since database is small and multiple apps are accessing 
same model often all database models are defined in models.py 
of *base* app along with application wide functionality to
increase maintainability.

## .env file format
`
SECRET_KEY=
STRIPE_API_KEY=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
`