# Digital Alumni Platform

A modern, full-stack Flask application for Alumni Relationship Management and Carrier Guidance.

## Features
- **Role-Based Access**: Admin, Faculty, Alumni, Student.
- **Authentication**: Secure Login/Signup with hashing.
- **Dashboards**: Custom dashboards for each role.
- **Jobs & Career**: Alumni post jobs, Faculty verify them, Students apply.
- **Gamification**: Points, Leaderboards, and Badges.
- **Modern UI**: Glassmorphism design with Bootstrap 5.

## Setup Instructions

### 1. Install Dependencies
Make sure you have Python installed. Run:
```bash
pip install -r requirements.txt
```

### 2. Configure Database
1. Make sure you have MySQL installed and running.
2. Create a database named `alumni_platform`.
3. Update `config.py` with your database credentials:
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/alumni_platform'
   ```

### 3. Run the Application
```bash
python run.py
```
The application will start at `http://localhost:5000`.

## Initial Login
- Create a new account via the **Sign Up** page.
- To make yourself an **Admin** or **Faculty**, you may need to manually update the `user` table in the database after registration, or simple tweak the registration logic temporarily.
