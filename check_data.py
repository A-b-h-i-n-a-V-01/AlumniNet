from app import create_app, db
from app.models import AlumniProfile, Job

def check():
    app = create_app()
    with app.app_context():
        alumni = AlumniProfile.query.all()
        jobs = Job.query.all()
        print(f"Total Alumni: {len(alumni)}")
        for a in alumni:
            a_jobs = Job.query.filter_by(user_id=a.id).all()
            print(f"  Alumni {a.user.username} (ID: {a.id}): {len(a_jobs)} jobs")
        print(f"Total Jobs: {len(jobs)}")

if __name__ == "__main__":
    check()
