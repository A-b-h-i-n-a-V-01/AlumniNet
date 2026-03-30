from app import create_app, db
from app.models import User, StudentProfile, Job

def verify():
    app = create_app()
    with app.app_context():
        # 1. Check a student profile (Alice Johnson)
        alice = User.query.filter_by(email='alice.johnson@student.com').first()
        if alice and alice.student_profile:
            print(f"Student {alice.username} Year: {alice.student_profile.current_year}, Sem: {alice.student_profile.semester}")
            
            # 2. Test job filtering logic
            student_yr_str = alice.student_profile.current_year
            jobs = Job.query.filter(Job.is_approved==True).filter(
                db.or_(Job.target_year == 'All', Job.target_year == student_yr_str)
            ).all()
            print(f"Jobs visible to Alice ({student_yr_str}): {len(jobs)}")
            if len(jobs) > 0:
                print("Job visibility fix verified!")
            else:
                print("Warning: No jobs visible. Checking all approved jobs...")
                all_approved = Job.query.filter_by(is_approved=True).all()
                for j in all_approved:
                    print(f"  Job: {j.title}, Target: {j.target_year}")

if __name__ == "__main__":
    verify()
