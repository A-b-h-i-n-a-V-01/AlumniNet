import os
from datetime import datetime, timedelta
from app import create_app, db, bcrypt
from app.models import User, AlumniProfile, StudentProfile, Job, Message, PointTransaction

def add_demo_data():
    app = create_app()
    with app.app_context():
        print("--- AlumniNet Demo Data Generation ---")
        
        # 1. Setup Demo Alumni Account
        demo_alumni_email = "alumni@gmail.com"
        demo_alumni_pass = "123"
        hashed_alumni_pw = bcrypt.generate_password_hash(demo_alumni_pass).decode('utf-8')
        
        user_alumni = User.query.filter_by(email=demo_alumni_email).first()
        if not user_alumni:
            print(f"Creating demo alumni: {demo_alumni_email}")
            user_alumni = User(
                username="Demo Alumni",
                email=demo_alumni_email,
                password=hashed_alumni_pw,
                role='alumni'
            )
            db.session.add(user_alumni)
            db.session.flush()
            
            profile_alumni = AlumniProfile(
                user_id=user_alumni.id,
                graduation_year=2015,
                degree="B.Tech CS",
                current_company="Microsoft",
                current_position="Senior Software Engineer",
                is_approved="Approved"
            )
            db.session.add(profile_alumni)
        else:
            print(f"Updating demo alumni password: {demo_alumni_email}")
            user_alumni.password = hashed_alumni_pw
            profile_alumni = user_alumni.alumni_profile
            profile_alumni.is_approved = "Approved"
        
        # Set points for leaderboard
        user_alumni.points = 150
        db.session.commit()
        
        # 2. Setup Demo Student Account
        demo_student_email = "student@gmail.com"
        demo_student_pass = "123"
        hashed_student_pw = bcrypt.generate_password_hash(demo_student_pass).decode('utf-8')
        
        user_student = User.query.filter_by(email=demo_student_email).first()
        if not user_student:
            print(f"Creating demo student: {demo_student_email}")
            user_student = User(
                username="Demo Student",
                email=demo_student_email,
                password=hashed_student_pw,
                role='student'
            )
            db.session.add(user_student)
            db.session.flush()
            
            profile_student = StudentProfile(
                user_id=user_student.id,
                enrollment_year=2021,
                department="Computer Science",
                cgpa=9.2
            )
            db.session.add(profile_student)
        else:
            print(f"Updating demo student password: {demo_student_email}")
            user_student.password = hashed_student_pw
        
        db.session.commit()
        
        # 3. Add Sample Job Listings with Deadlines
        print("Adding sample job listings with deadlines...")
        
        # Clear existing jobs by this user if any to keep it clean
        Job.query.filter_by(user_id=profile_alumni.id).delete()
        
        now = datetime.utcnow()
        future_dates = [now + timedelta(days=d) for d in [15, 30, 45, 60, 90]]
        
        jobs_to_add = [
            {
                "title": "Machine Learning Engineer",
                "company": "Microsoft",
                "location": "Redmond / Remote",
                "type": "Full-time",
                "link": "https://careers.microsoft.com/ml-engineer",
                "target": "2024, 2025",
                "deadline": future_dates[0]
            },
            {
                "title": "Front-end Developer (React)",
                "company": "Startup Hub",
                "location": "Bangalore / Hybrid",
                "type": "Internship",
                "link": "https://startuphub.io/careers/frontend",
                "target": "2025, 2026",
                "deadline": future_dates[1]
            },
            {
                "title": "DevOps Architect",
                "company": "CloudScape",
                "location": "Remote",
                "type": "Full-time",
                "link": "https://cloudscape.com/jobs/devops",
                "target": "All Batches",
                "deadline": future_dates[2]
            },
            {
                "title": "Data Science Research Fellow",
                "company": "Academic Lab",
                "location": "London, UK",
                "type": "Contract",
                "link": "https://academic-lab.edu/fellowship",
                "target": "Postgraduates",
                "deadline": future_dates[3]
            },
            {
                "title": "Cybersecurity Consultant",
                "company": "SecureNet",
                "location": "Mumbai, India",
                "type": "Full-time",
                "link": "https://securenet.com/careers/cybersec",
                "target": "2023, 2024",
                "deadline": future_dates[4]
            }
        ]
        
        for j_info in jobs_to_add:
            job = Job(
                title=j_info['title'],
                company=j_info['company'],
                location=j_info['location'],
                job_type=j_info['type'],
                description=f"This is a sample description for {j_info['title']} at {j_info['company']}. We are looking for talented {j_info['target']} candidates.",
                apply_link=j_info['link'],
                target_year=j_info['target'],
                application_deadline=j_info['deadline'],
                is_approved=True,
                user_id=profile_alumni.id
            )
            db.session.add(job)
            
        db.session.commit()
        
        # 4. Add Sample Chat Conversations
        print("Adding sample chat conversations...")
        
        # Clear existing messages between these two
        Message.query.filter(
            db.or_(
                db.and_(Message.sender_id == user_alumni.id, Message.recipient_id == user_student.id),
                db.and_(Message.sender_id == user_student.id, Message.recipient_id == user_alumni.id)
            )
        ).delete()
        
        conversation = [
            (user_student.id, user_alumni.id, "Hello! I saw your post for the ML Engineer role at Microsoft. Can you share some insights?"),
            (user_alumni.id, user_student.id, "Hi! Sure. We focus heavily on deep learning and model optimization. Do you have experience with PyTorch?"),
            (user_student.id, user_alumni.id, "Yes, I've used it in my university projects. Is there any specific coding round I should prepare for?"),
            (user_alumni.id, user_student.id, "Yes, expect a few LeetCode medium questions and some system design basics."),
            (user_student.id, user_alumni.id, "Thank you so much! That helps a lot.")
        ]
        
        for i, (sid, rid, content) in enumerate(conversation):
            msg = Message(
                sender_id=sid,
                recipient_id=rid,
                content=content,
                timestamp=datetime.utcnow() - timedelta(minutes=10 - i)
            )
            db.session.add(msg)
            
        db.session.commit()
        
        # 5. Leaderboard - Give points to other users to create a competitive list
        print("Populating leaderboard with more users...")
        
        other_alumni_emails = ["top_alumni@gmail.com", "runner_up@gmail.com", "contributor@gmail.com"]
        points_list = [250, 180, 120]
        
        for email, pts in zip(other_alumni_emails, points_list):
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(
                    username=email.split('@')[0].replace('_', ' ').title(),
                    email=email,
                    password=hashed_alumni_pw, # use same pw for convenience
                    role='alumni'
                )
                db.session.add(user)
                db.session.flush()
                
                profile = AlumniProfile(
                    user_id=user.id,
                    graduation_year=2010,
                    degree="Master of Tech",
                    is_approved="Approved"
                )
                db.session.add(profile)
            user.points = pts
            
            # Record a transaction just in case
            trans = PointTransaction(
                user_id=user.id,
                action="demo_contribution",
                amount=pts,
                timestamp=datetime.utcnow()
            )
            db.session.add(trans)
            
        db.session.commit()
        
        print("\n--- Demo Data Generation Complete! ---")
        print(f" Demo Alumni Login: {demo_alumni_email} / {demo_alumni_pass}")
        print(f" Demo Student Login: {demo_student_email} / {demo_student_pass}")

if __name__ == "__main__":
    add_demo_data()
