from app import create_app, db
from app.models import AlumniProfile, Job
from datetime import datetime

def add_jobs():
    app = create_app()
    with app.app_context():
        # Get Alumni profiles
        a1 = AlumniProfile.query.get(1) # akalumni
        a2 = AlumniProfile.query.get(2) # John Doe
        a3 = AlumniProfile.query.get(3) # Jane Smith
        a4 = AlumniProfile.query.get(4) # Robert Brown
        
        more_jobs = [
            {
                "title": "Graduate Trainee Engineer",
                "company": "TCS",
                "location": "Kochi, Kerala",
                "description": "Excellent opportunity for freshers! Joining our development team in Kochi. Focus on Java, Spring, and Web Technologies.",
                "apply_link": "https://www.tcs.com/careers/india/entry-level",
                "target_year": "2024 batch",
                "user_id": a1.id if a1 else 1 # default to ID 1 if not found
            },
            {
                "title": "Machine Learning Engineer",
                "company": "Google",
                "location": "Remote",
                "description": "Help us build the next generation of AI products! Proficiency in TensorFlow, PyTorch and large-scale data processing is required.",
                "apply_link": "https://careers.google.com/jobs/results/ml-engineer-ai",
                "target_year": "All Batches",
                "user_id": a2.id if a2 else 2
            },
            {
                "title": "Product Analyst",
                "company": "Meta",
                "location": "London / Remote",
                "description": "Bridge the gap between business and technology. Analyze product metrics and drive growth. Excellent SQL skills mandatory.",
                "apply_link": "https://meta.com/careers/analyst",
                "target_year": "2023 batch",
                "user_id": a3.id if a3 else 3
            },
            {
                "title": "Cloud Solutions Architect",
                "company": "AWS",
                "location": "Seattle, WA / Remote",
                "description": "Design and build cloud-native applications on AWS. Help customers migrate datasets and services to the cloud.",
                "apply_link": "https://amazon.jobs/en/jobs/cloud-architect",
                "target_year": "Experienced",
                "user_id": a4.id if a4 else 4
            },
            {
                "title": "Full Stack Developer",
                "company": "Infosys",
                "location": "Trivandrum, Kerala",
                "description": "Join our dynamic development team in Trivandrum. Modern web tech stack - React, Node.js, and MongoDB.",
                "apply_link": "https://www.infosys.com/careers/india/entry-level",
                "target_year": "2024/2025",
                "user_id": a1.id if a1 else 1
            }
        ]

        for j in more_jobs:
            # Check if this job title already exists for this alumni to avoid duplicates
            existing = Job.query.filter_by(title=j['title'], user_id=j['user_id']).first()
            if not existing:
                print(f"Adding extra job: {j['title']} at {j['company']}")
                job = Job(
                    title=j['title'],
                    company=j['company'],
                    location=j['location'],
                    description=j['description'],
                    apply_link=j['apply_link'],
                    target_year=j['target_year'],
                    is_approved=True,
                    user_id=j['user_id']
                )
                db.session.add(job)
        
        db.session.commit()
        print("\nExtra jobs added successfully!")

if __name__ == "__main__":
    add_jobs()
