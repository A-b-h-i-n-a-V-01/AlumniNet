from app import create_app, db
from app.models import User, Message, AlumniProfile, StudentProfile
from datetime import datetime, timedelta

def add_data():
    app = create_app()
    with app.app_context():
        # 1. Create Abhinav if not exists
        abhinav = User.query.filter_by(email='alumni@gmail.com').first()
        if not abhinav:
            from app import bcrypt
            hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
            abhinav = User(username='Abhinav', email='alumni@gmail.com', password=hashed_pw, role='alumni')
            db.session.add(abhinav)
            db.session.flush()
            
            profile = AlumniProfile(
                user_id=abhinav.id,
                degree='B.Tech CSE',
                graduation_year=2018,
                current_company='Google',
                current_position='Senior Software Engineer',
                is_approved='Approved'
            )
            db.session.add(profile)
            abhinav.points = 500
            print("Created user Abhinav (alumni@gmail.com)")
        else:
            print("User Abhinav already exists")

        # 2. Find some other users to talk to
        alice = User.query.filter_by(email='alice.johnson@student.com').first()
        bob = User.query.filter_by(email='bob.wilson@student.com').first()
        john = User.query.filter_by(email='john.doe@alumni.com').first()

        now = datetime.utcnow()

        messages = [
            # With Alice (Student)
            (alice, abhinav, "Hi Abhinav! I saw your profile and noticed you are at Google. Can you give me some tips for the interview?", now - timedelta(days=2)),
            (abhinav, alice, "Hey Alice! Sure, I'd love to help. Have you started preparing for DSA?", now - timedelta(days=1, hours=22)),
            (alice, abhinav, "Yes, I'm practicing on LeetCode. Which topics should I focus more on?", now - timedelta(days=1, hours=20)),
            (abhinav, alice, "Focus heavily on Graphs and Dynamic Programming. Also, make sure your projects are solid.", now - timedelta(hours=5)),
            
            # With Bob (Student)
            (bob, abhinav, "Hello sir, I'm interested in the Backend role you posted. Can you refer me?", now - timedelta(days=3)),
            (abhinav, bob, "Hi Bob, send me your resume. I'll take a look and see if I can refer you.", now - timedelta(days=2, hours=10)),
            
            # With John Doe (Fellow Alumni)
            (john, abhinav, "Hey Abhinav, long time! Are you coming for the next alumni meet?", now - timedelta(days=5)),
            (abhinav, john, "Hey John! Yes, I'll be there. Excited to catch up with the batch!", now - timedelta(days=4))
        ]

        for sender, recipient, content, ts in messages:
            if sender and recipient:
                # Check if message already exists to avoid duplicates
                existing = Message.query.filter_by(sender_id=sender.id, recipient_id=recipient.id, content=content).first()
                if not existing:
                    msg = Message(sender_id=sender.id, recipient_id=recipient.id, content=content, timestamp=ts, is_read=True)
                    db.session.add(msg)

        db.session.commit()
        print("Messages added successfully for Abhinav!")

if __name__ == "__main__":
    add_data()
