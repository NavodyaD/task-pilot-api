# Classroom Management API

A small FastAPI learning project that follows a simple layered structure similar to a Spring Boot application. It lets teachers manage classrooms, subjects, assessments and marks, while students can join classrooms and view only their own results.

## Main features

- Register and log in as a `TEACHER` or `STUDENT`.
- JWT bearer-token authentication.
- Teachers create and manage only their own classrooms.
- Teachers enrol students, create subjects and assessments, and record or update marks.
- Students can see their enrolled classrooms, subjects, assessments and their own marks.
- Input validation and useful HTTP error responses.

## Project structure

```text
app/
  config/          Database configuration
  models/          SQLAlchemy table models and relationships
  schemas/         Pydantic request validation models
  repository/      Database query/save code
  service/         Business logic layer
  controller/      FastAPI routes
  auth.py          Password hashing, JWT and role checks
  main.py          Application startup and route registration
```

## Data model

```text
User (TEACHER) 1 --- many Classroom
Classroom       1 --- many Subject
Classroom       many --- many User (STUDENT), through ClassroomStudent
Subject         1 --- many Assessment
Assessment      1 --- many Mark
User (STUDENT)  1 --- many Mark
```

## Setup and run

1. Create and activate a virtual environment.
2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create a `.env` file. PostgreSQL example:

   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/classroom_management
   SECRET_KEY=replace-with-a-long-random-secret
   ```

   For a quick local learning setup, SQLite also works:

   ```env
   DATABASE_URL=sqlite:///./classroom_management.db
   ```

4. Start the API:

   ```powershell
   uvicorn app.main:app --reload
   ```

5. Open Swagger UI at `http://127.0.0.1:8000/docs`.

## Authentication flow

1. Register at `POST /auth/register` with a name, email, password and role.
2. Log in at `POST /auth/login`.
3. Copy the returned `access_token`.
4. In Swagger, click **Authorize** and enter `Bearer <access_token>`.
5. Call protected endpoints. The API reads the user and role from the token.

Only a `TEACHER` can create classrooms, add students, create academic content, or record marks. Teachers also pass an ownership check, so one teacher cannot manage another teacher’s classroom.

## Main endpoints

| Area | Method | Endpoint | Who can use it |
| --- | --- | --- | --- |
| Authentication | POST | `/auth/register` | Public |
| Authentication | POST | `/auth/login` | Public |
| Authentication | GET | `/auth/me` | Logged-in user |
| Classrooms | POST | `/classrooms` | Teacher |
| Classrooms | GET | `/classrooms` | Teacher or student |
| Enrolment | POST | `/classrooms/{id}/students` | Classroom teacher |
| Enrolment | GET | `/classrooms/{id}/students` | Classroom teacher |
| Subjects | POST | `/classrooms/{id}/subjects` | Classroom teacher |
| Subjects | GET | `/classrooms/{id}/subjects` | Teacher owner or enrolled student |
| Assessments | POST | `/subjects/{id}/assessments` | Subject classroom teacher |
| Assessments | GET | `/subjects/{id}/assessments` | Teacher owner or enrolled student |
| Marks | POST | `/assessments/{id}/marks` | Assessment classroom teacher |
| Marks | GET | `/assessments/{id}/marks` | Teacher sees all; student sees own |

## Example request order

1. Register a teacher and a student.
2. Log in as the teacher.
3. Create a classroom with `POST /classrooms`.
4. Enrol the student using `POST /classrooms/{classroom_id}/students`.
5. Add a subject, then add an assessment under that subject.
6. Record the student’s score with `POST /assessments/{assessment_id}/marks`.
7. Log in as the student and request `GET /assessments/{assessment_id}/marks` to view that student’s result.

## Error handling and validation

- Pydantic validates emails, required names, IDs, password length, and positive maximum marks before business logic runs.
- Duplicate emails and duplicate enrolments return `409 Conflict`.
- Missing resources return `404 Not Found`.
- Invalid logins or missing tokens return `401 Unauthorized`.
- Role or classroom ownership failures return `403 Forbidden`.
- A score cannot be negative, greater than the assessment maximum, or recorded for a student outside the classroom.

## Notes for learning

The application creates tables at startup using `Base.metadata.create_all()`. This is convenient for a learning project. For production work, introduce Alembic migrations, stronger secret management, tests, pagination, and a more complete response-schema layer.
