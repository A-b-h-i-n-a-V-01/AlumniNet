from app import create_app, db
from app.models import Job

def fix_jobs():
    app = create_app()
    with app.app_context():
        # Map old free-text target_years to the new standard choices
        # choices are: 'All', '1st Year', '2nd Year', '3rd Year', '4th Year'
        
        job_map = {
            "Software Engineering Intern": "1st Year",
            "Junior Backend Developer": "4th Year",
            "Graduate Data Analyst": "4th Year",
            "SDE-1 (Java/Spring)": "All",
            "Graduate Trainee Engineer": "4th Year",
            "Machine Learning Engineer": "All",
            "Product Analyst": "3rd Year",
            "Cloud Solutions Architect": "All",
            "Full Stack Developer": "1st Year"
        }

        updated = 0
        for title, tag in job_map.items():
            job = Job.query.filter_by(title=title).first()
            if job:
                job.target_year = tag
                updated += 1
        
        db.session.commit()
        print(f"Updated {updated} sample jobs with standard year tags.")

if __name__ == "__main__":
    fix_jobs()
