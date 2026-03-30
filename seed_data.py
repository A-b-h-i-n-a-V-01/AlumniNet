import os
import sys
from datetime import datetime
from app import create_app, db, bcrypt
from app.models import User, AlumniProfile, StudentProfile, Job, Message

def seed():
    app = create_app()
    with app.app_context():
        print("--- AlumniNet Database Seeding ---")
        
        # 0. clear existing data (except admin)
        print("Wait! This script will not delete users unless explicitly told to. Proceeding to add data...")
        
        # 1. SAMPLE ALUMNI
        alumni_data = [
            {
                "email": "john.doe@google.com",
                "username": "John Doe",
                "company": "Google",
                "position": "Software Engineer",
                "degree": "B.Tech Computer Science",
                "grad_year": 2018,
                "linkedin": "https://www.linkedin.com/in/john-doe-google"
            },
            {
                "email": "jane.smith@meta.com",
                "username": "Jane Smith",
                "company": "Meta",
                "position": "Senior Data Scientist",
                "degree": "M.Tech AI/ML",
                "grad_year": 2016,
                "linkedin": "https://www.linkedin.com/in/jane-smith-meta"
            },
            {
                "email": "robert.brown@amazon.com",
                "username": "Robert Brown",
                "company": "Amazon",
                "position": "Technical Product Manager",
                "degree": "B.Tech IT",
                "grad_year": 2019,
                "linkedin": "https://www.linkedin.com/in/robert-brown-amazon"
            }
        ]
        
        hashed_pw = bcrypt.generate_password_hash("password123").decode('utf-8')
        
        created_alumni_profiles = []
        for a in alumni_data:
            existing_user = User.query.filter_by(email=a['email']).first()
            if not existing_user:
                print(f"Creating alumni: {a['username']} ({a['email']})")
                user = User(
                    username=a['username'],
                    email=a['email'],
                    password=hashed_pw,
                    role='alumni'
                )
                db.session.add(user)
                db.session.flush() # get user id
                
                profile = AlumniProfile(
                    user_id=user.id,
                    graduation_year=a['grad_year'],
                    degree=a['degree'],
                    current_company=a['company'],
                    current_position=a['position'],
                    linkedin_url=a['linkedin'],
                    is_approved="Approved" # Pre-approve for demo
                )
                db.session.add(profile)
                db.session.flush()
                created_alumni_profiles.append(profile)
            else:
                print(f"Alumni exists: {a['username']}")
                created_alumni_profiles.append(existing_user.alumni_profile)
        
        db.session.commit()
        
        # 2. SAMPLE JOBS
        jobs_data = [
            {
                "title": "Software Engineering Intern",
                "company": "Google",
                "location": "Mountain View / Remote",
                "description": "Join our cloud team as a summer intern. You will work on scalable backend services and distributed systems.",
                "apply_link": "https://careers.google.com/jobs/results/internship-cloud-backend",
                "target_year": "2024, 2025",
                "author_profile": created_alumni_profiles[0]
            },
            {
                "title": "Junior Backend Developer",
                "company": "Google",
                "location": "Bangalore, India",
                "description": "Looking for entry-level developers proficient in Python and C++. You'll be part of the Search Infrastructure team.",
                "apply_link": "https://careers.google.com/jobs/results/junior-backend",
                "target_year": "2023 batch",
                "author_profile": created_alumni_profiles[0]
            },
            {
                "title": "Graduate Data Analyst",
                "company": "Meta",
                "location": "Dublin / Remote",
                "description": "Analyze user behavior data to drive platform improvements. Proficiency in SQL and R/Python is required.",
                "apply_link": "https://meta.com/careers/data-analyst",
                "target_year": "2023, 2024",
                "author_profile": created_alumni_profiles[1]
            },
            {
                "title": "SDE-1 (Java/Spring)",
                "company": "Amazon",
                "location": "Hyderabad, India",
                "description": "Work on high-availability fulfillment services. Strong understanding of OOPS and Data Structures needed.",
                "apply_link": "https://amazon.jobs/en/jobs/254422",
                "target_year": "All Batches",
                "author_profile": created_alumni_profiles[2]
            }
        ]
        
        for j in jobs_data:
            existing_job = Job.query.filter_by(title=j['title'], user_id=j['author_profile'].id).first()
            if not existing_job:
                print(f"Adding job: {j['title']} at {j['company']}")
                job = Job(
                    title=j['title'],
                    company=j['company'],
                    location=j['location'],
                    description=j['description'],
                    apply_link=j['apply_link'],
                    target_year=j['target_year'],
                    is_approved=True,
                    user_id=j['author_profile'].id
                )
                db.session.add(job)
        
        db.session.commit()
        
        # 3. SAMPLE STUDENTS
        student_data = [
            {
                "email": "alice.johnson@student.com",
                "username": "Alice Johnson",
                "dept": "Computer Science",
                "year": 2024
            },
            {
                "email": "bob.wilson@student.com",
                "username": "Bob Wilson",
                "dept": "Information Technology",
                "year": 2025
            }
        ]
        
        created_student_users = []
        for s in student_data:
            existing_student = User.query.filter_by(email=s['email']).first()
            if not existing_student:
                print(f"Creating student: {s['username']}")
                user = User(
                    username=s['username'],
                    email=s['email'],
                    password=hashed_pw,
                    role='student'
                )
                db.session.add(user)
                db.session.flush()
                
                profile = StudentProfile(
                    user_id=user.id,
                    enrollment_year=s['year'],
                    department=s['dept'],
                    cgpa=8.5
                )
                db.session.add(profile)
                db.session.flush()
                created_student_users.append(user)
            else:
                print(f"Student exists: {s['username']}")
                created_student_users.append(existing_student)
        
        db.session.commit()
        
        # 4. SAMPLE MESSAGES
        if created_student_users and created_alumni_profiles:
            # Student 1 to Alumni 1
            msg1 = Message(
                sender_id=created_student_users[0].id,
                recipient_id=created_alumni_profiles[0].user_id,
                content="Hi John! I saw the Software Engineering Intern post at Google. Could you please share some tips for the interview?",
                timestamp=datetime.utcnow()
            )
            # Alumni 1 Reply
            msg2 = Message(
                sender_id=created_alumni_profiles[0].user_id,
                recipient_id=created_student_users[0].id,
                content="Hey Alice! Sure, focusing on Data Structures and Algorithms is key. Also, be sure to understand Google's coding standards.",
                timestamp=datetime.utcnow()
            )
            db.session.add_all([msg1, msg2])
            print("Added sample messages.")
        
        db.session.commit()
        print("\n--- Seeding Complete! ---")
        print(" Demo Users:")
        print("  1. Alumni: john.doe@google.com / password123")
        print("  2. Student: alice.johnson@student.com / password123")
        print("  3. Admin: admin@alumninet.com / admin@123 (if setup_db was run)")

if __name__ == "__main__":
    seed()
