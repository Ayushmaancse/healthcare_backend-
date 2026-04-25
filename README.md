# Healthcare Backend API

## Overview
This is a backend system for a healthcare application built using Django, Django REST Framework (DRF), and PostgreSQL. It features secure JWT authentication and allows authenticated users to manage patients, doctors, and patient-doctor mappings.

## Core Requirements
**Django & DRF**: Used natively for the backend structure.
**PostgreSQL**: Integrated as the primary database mapped seamlessly via configuration.
 **JWT Authentication**: Implemented securely via `djangorestframework-simplejwt`.
 **RESTful APIs**: Built fully realized CRUD endpoints for Patients, Doctors, and Mapping.
 **Django ORM**: Utilized strictly for all database modeling, including relational ForeignKeys.
**Error Handling & Validation**: Native DRF validation augmented with custom object-level ownership checks.
 **Environment Variables**: Sensitive data secured using `.env` (`django-environ`).

## Tech Stack
- **Framework**: Django & Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Authentication**: JWT (djangorestframework-simplejwt)



## Setup Instructions

> **Note:** For ease of testing and to skip local database setup, this project is connected to a cloud-hosted PostgreSQL database via Neon. You can run `python manage.py runserver` and test the APIs immediately without any local Postgres configuration!

1. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Database (Environment Variables)**:
   This project securely manages database connections using `django-environ`. If you want to use your own local PostgreSQL database instead of the cloud-hosted Neon database, create a `.env` file in the root of the project and provide your credentials using this format:
   ```env
   SECRET_KEY=your-secret-django-key
   DEBUG=True
   
   # To use a local DB, construct your connection string like this:
   # postgres://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE_NAME>
   DATABASE_URL=postgres://postgres:postgres@localhost:5432/healthcare_db
   ```
   *Note: If testing locally, make sure your PostgreSQL server is running and you have explicitly created the database matching your URL (e.g., `healthcare_db`) before migrating.*

4. **Run Database Migrations**:
   Initialize the PostgreSQL tables by running:
   ```bash
   python manage.py makemigrations api
   python manage.py migrate
   ```

5. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
   The backend will now be live at `http://127.0.0.1:8000/`.

---

## Testing the APIs (Postman)
Once the server is running, you can hit the following endpoints. 

### 1. Authentication APIs
- `POST /api/auth/register/` - Register a new user with `name`, `email`, and `password`.
- `POST /api/auth/login/` - Log in and receive your JWT token. *(Note: Pass the user's email as the `username` key in the request body).*

**For the remaining APIs, include your JWT token in the `Authorization` header as a Bearer token:**
`Authorization: Bearer <your_jwt_token>`

### 2. Patient Management APIs
*Patients are securely tied to the user that created them.*
- `POST /api/patients/` - Add a new patient.
- `GET /api/patients/` - Retrieve all patients created by you.
- `GET /api/patients/<id>/` - Get details of a specific patient.
- `PUT /api/patients/<id>/` - Update patient details.
- `DELETE /api/patients/<id>/` - Delete a patient record.

### 3. Doctor Management APIs
- `POST /api/doctors/` - Add a new doctor.
- `GET /api/doctors/` - Retrieve all doctors.
- `GET /api/doctors/<id>/` - Get details of a specific doctor.
- `PUT /api/doctors/<id>/` - Update doctor details.
- `DELETE /api/doctors/<id>/` - Delete a doctor record.

### 4. Patient-Doctor Mapping APIs
- `POST /api/mappings/` - Assign a doctor to a patient.
- `GET /api/mappings/` - Retrieve all patient-doctor mappings.
- `GET /api/mappings/<patient_id>/` - Get all doctors assigned to a specific patient.
- `DELETE /api/mappings/<id>/` - Remove a doctor from a patient.

---

## Architecture, Design Patterns & Tradeoffs

To ensure a modular, secure, and production-ready codebase, the following patterns and architectural decisions were heavily prioritized:

1. **12-Factor App Methodology**: Sensitive configurations (Database URLs, Secret Keys) are strictly decoupled from the codebase using `django-environ`, ensuring enterprise-grade credential security.
2. **Model-Serializer-View Architecture**: An API-focused adaptation of the traditional MVC pattern. Separation of concerns is rigidly enforced: `models.py` exclusively manages the PostgreSQL schemas, `serializers.py` manages JSON translation and explicit data validation, and `views.py` acts purely as the permission controller.
3. **Stateless JWT Authentication**: Opted for `djangorestframework-simplejwt` over traditional Django session cookies. **Tradeoff:** Access tokens cannot be instantaneously revoked without a complex blocklist, but this ensures the API is 100% stateless, fully compatible with mobile/React clients, and scales infinitely.
4. **DRF ViewSets & Data Abstraction**: Utilized `ModelViewSet` and `DefaultRouter` over manual APIViews. **Tradeoff:** Higher initial abstraction, but significantly reduces boilerplate code and automatically guarantees perfectly structured RESTful endpoints.
5. **Object-Level Security Injection**: By hooking directly into the `get_queryset()` lifecycle and the serializer's `validate_patient()` method, we guarantee that authenticated users can securely only view, map, and modify their perfectly isolated patient records.
