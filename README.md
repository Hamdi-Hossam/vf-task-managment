# Requirements:
Make sure you have the following installed on your system:

- Python 3.x
- pip (Python package manager)
- Virtualenv (optional but recommended)

# Setup Instructions:

#### **Step 1: Create and Activate a Virtual Environment**

- python -m venv env  
- env/Scripts/activate

#### **Step 2: Install Dependencies**

- pip install -r requirements.txt

#### **Step 3: Run Migrations**

- python manage.py makemigrations  
- python manage.py migrate

#### **Step 4: Start the Development Server**

- python manage.py runserver

# Additional Needed Setup Instructions:

### Note: These are required for the report generation

- Extract the zipped redis folder

#### **Step 1: Run Redis Server**

#### **Step 2: Run Celery Worker**

- celery -A task_manager worker --loglevel=info --pool=solo

#### **Step 3: Run Celery Beat**

- celery -A task_manager beat --loglevel=info


# Example API Requests and Responses:

### User End points

**POST** `api/auth/signup/`
#### Note: If no provided role field it will be by default user 
```json
{
    "username":"Hamdi",
    "email":"hamdihossam461@gmail.com",
    "password":"1234"
}
```
**Response:**
*Status Code:* `201 Created`
```json
{
    "message": "User registered successfully"
}
```


**POST** `api/auth/signin/`
```json
{
    "email":"hamdihossam461@gmail.com",
    "password":"1234"
}
```
**Response:**
*Status Code:* `200 Ok`
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzODU2OTk2LCJpYXQiOjE3MzM4NTY2OTYsImp0aSI6ImJhODVhNDc0OTAyOTQyODg4ZWI0NmNkOGIxZGI2ZDBmIiwidXNlcl9pZCI6NH0.gIbEst9oa0zQ4a8oDcnEM6WDJNiJ6pltA15hhd5oymw",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMzk0MzA5NiwiaWF0IjoxNzMzODU2Njk2LCJqdGkiOiI2OTAzMzZlYTQ4MmM0YWE5YTFkNzlmMjY4MTc2NDUyNiIsInVzZXJfaWQiOjR9.Alr3pGEF0mNTMN2HMcLqZIWoU6hNmj7qEdREWadSZ2o"
}
```

### Tasks End points

**GET** `/api/tasks?status=pending&start_date="2024-12-15T10:00:00Z"&end_date="2024-12-16T10:00:00Z"`

**Response:**
*Status Code:* `200 Ok`
```json
[
    {
        "id": 2,
        "title": "Task 1",
        "description": "Description of task",
        "start_date": "2024-12-15T10:00:00Z",
        "due_date": "2024-12-16T10:00:00Z",
        "completion_date": null,
        "status": "pending",
        "user": 1,
        "created_at": "2024-12-10T14:02:33.354969Z",
        "deleted_at": null
    },
    {
        "id": 3,
        "title": "Task 2",
        "description": "Description of task",
        "start_date": "2024-12-14T10:00:00Z",
        "due_date": "2024-12-16T10:00:00Z",
        "completion_date": null,
        "status": "pending",
        "user": 1,
        "created_at": "2024-12-10T14:02:57.530283Z",
        "deleted_at": null
    },
]
```

**POST** `/api/tasks/create/`
```json
{
    "title": "Task to be emailed to weekly subscribers",
    "description": "Description of task",
    "start_date": "2024-12-1T10:00:00Z",
    "due_date": "2024-12-5T10:00:00Z"
}
```
**Response:**
*Status Code:* `201 Created`
```json
{
    "id": 17,
    "title": "Task to be emailed to weekly subscribers",
    "description": "Description of task",
    "start_date": "2024-12-01T10:00:00Z",
    "due_date": "2024-12-05T10:00:00Z",
    "completion_date": null,
    "status": "pending",
    "user": 1,
    "created_at": "2024-12-10T18:50:46.684538Z",
    "deleted_at": null
}
```

**PUT** `/api/tasks/{id}/`
```json
{
  "title": "Updated Task 1",
  "description": "This task has been updated",
  "start_date": "2024-12-15T10:00:00Z",
  "due_date": "2024-12-17T10:00:00Z",
  "status": "completed"
}
```
**Response:**
*Status Code:* `200 Ok`
```json
{
    "id": 1,
    "title": "Updated Task 1",
    "description": "This task has been updated",
    "start_date": "2024-12-15T10:00:00Z",
    "due_date": "2024-12-17T10:00:00Z",
    "completion_date": null,
    "status": "completed",
    "user": 1,
    "created_at": "2024-12-10T13:27:34.249897Z",
    "deleted_at": null
}
```

**DELETE** `/api/tasks/{id}/delete/`

**Response:**
*Status Code:* `204 No Content`
```json
{
    "detail": "Task deleted successfully."
}
```

**DELETE** `/api/tasks/batch-delete/`
```json
{
  "start_date": "2024-12-01T00:00:00Z",
  "end_date": "2024-12-31T23:59:59Z"
}
```
**Response:**
*Status Code:* `204 No Content`
```json
{
    "detail": "7 tasks deleted successfully."
}
```

**POST** `/api/tasks/restore-last-deleted/`

**Response:**
*Status Code:* `200 Ok`
```json
{
    "id": 8,
    "title": "Task to be Restored",
    "description": "Description of task",
    "start_date": "2024-12-10T10:00:00Z",
    "due_date": "2024-12-16T10:00:00Z",
    "completion_date": null,
    "status": "pending",
    "user": 1,
    "created_at": "2024-12-10T14:18:07.441694Z",
    "deleted_at": null
}
```


### Subscription End points

**POST** `/api/subscribe/`
```json
{
    "start_date": "2024-12-10T08:00:00Z",
    "frequency": "weekly",
    "report_time": 8
}
```
**Response:**
*Status Code:* `200 Ok`
```json
{
    "message": "Subscription created.",
    "data": {
        "start_date": "2024-12-10T08:00:00Z",
        "frequency": "weekly",
        "report_time": 8
    }
}
```

**DELETE** `/api/unsubscribe/`

**Response:**
*Status Code:* `200 Ok`
```json
{
    "message": "Unsubscribed successfully."
}
```
# Note: All of the above endpoints are authenticated so you need the token to be able to access it except the signup and sigin, Signin for the token.