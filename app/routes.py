from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import User, Job, AlumniProfile, StudentProfile, Certificate
from app.forms import RegistrationForm, LoginForm, JobPostForm, AlumniProfileForm, StudentProfileForm

# Public Routes
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# Auth Routes
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.flush() 

        if user.role == 'alumni':
            profile = AlumniProfile(user_id=user.id, graduation_year=2020, degree='B.Tech')
            db.session.add(profile)
        elif user.role == 'student':
            profile = StudentProfile(user_id=user.id, enrollment_year=2024, department='CSE')
            db.session.add(profile)
        
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

def logout():
    logout_user()
    return redirect(url_for('login'))

# Main App Routes
@login_required
def dashboard():
    if current_user.role == 'admin':
        users_count = User.query.count()
        jobs_count = Job.query.count()
        pending_alumni = AlumniProfile.query.filter_by(is_approved='Pending').count()
        return render_template('dashboard.html', users_count=users_count, jobs_count=jobs_count, pending_alumni=pending_alumni)
    
    elif current_user.role == 'faculty':
        pending_jobs = Job.query.filter_by(is_approved=False).all()
        pending_alumni = AlumniProfile.query.filter_by(is_approved='Pending').all()
        return render_template('dashboard.html', pending_jobs=pending_jobs, pending_alumni=pending_alumni)
    
    elif current_user.role == 'alumni':
        my_jobs = Job.query.filter_by(user_id=current_user.alumni_profile.id).all()
        return render_template('dashboard.html', jobs=my_jobs, profile=current_user.alumni_profile)
    
    elif current_user.role == 'student':
        recent_jobs = Job.query.filter_by(is_approved=True).order_by(Job.date_posted.desc()).limit(5).all()
        return render_template('dashboard.html', jobs=recent_jobs)
    
    return render_template('dashboard.html')

@login_required
def jobs():
    jobs = Job.query.filter_by(is_approved=True).all()
    return render_template('jobs.html', jobs=jobs)

@login_required
def new_job():
    if current_user.role != 'alumni':
        abort(403)
    form = JobPostForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, company=form.company.data, 
                  location=form.location.data, description=form.description.data,
                  apply_link=form.apply_link.data, author=current_user.alumni_profile)
        db.session.add(job)
        db.session.commit()
        flash('Job posted! Waiting for faculty approval.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_job.html', title='New Job', form=form)

@login_required
def approve_job(job_id):
    if current_user.role not in ['faculty', 'admin']:
        abort(403)
    job = Job.query.get_or_404(job_id)
    job.is_approved = True
    job.author.user.points += 10
    db.session.commit()
    flash('Job verified and published! Author awarded 10 points.', 'success')
    return redirect(url_for('dashboard'))

@login_required
def approve_alumni(profile_id):
    if current_user.role not in ['faculty', 'admin']:
        abort(403)
    profile = AlumniProfile.query.get_or_404(profile_id)
    profile.is_approved = 'Approved'
    profile.user.points += 50
    db.session.commit()
    flash('Alumni profile verified! User awarded 50 points.', 'success')
    return redirect(url_for('dashboard'))

@login_required
def profile():
    form = None
    if current_user.role == 'alumni':
        form = AlumniProfileForm()
        if form.validate_on_submit():
            current_user.alumni_profile.degree = form.degree.data
            current_user.alumni_profile.graduation_year = form.graduation_year.data
            current_user.alumni_profile.current_company = form.current_company.data
            current_user.alumni_profile.current_position = form.current_position.data
            current_user.alumni_profile.linkedin_url = form.linkedin_url.data
            current_user.points += 5
            db.session.commit()
            flash('Profile Updated! +5 Points', 'success')
            return redirect(url_for('profile'))
        elif request.method == 'GET':
            form.degree.data = current_user.alumni_profile.degree
            form.graduation_year.data = current_user.alumni_profile.graduation_year
            form.current_company.data = current_user.alumni_profile.current_company
            form.current_position.data = current_user.alumni_profile.current_position
            form.linkedin_url.data = current_user.alumni_profile.linkedin_url

    elif current_user.role == 'student':
        form = StudentProfileForm()
        if form.validate_on_submit():
            current_user.student_profile.department = form.department.data
            current_user.student_profile.enrollment_year = form.enrollment_year.data
            current_user.student_profile.cgpa = float(form.cgpa.data) if form.cgpa.data else 0.0
            current_user.points += 5
            db.session.commit()
            flash('Profile Updated! +5 Points', 'success')
            return redirect(url_for('profile'))
        elif request.method == 'GET':
            form.department.data = current_user.student_profile.department
            form.enrollment_year.data = current_user.student_profile.enrollment_year
            form.cgpa.data = current_user.student_profile.cgpa

    return render_template('profile.html', title='Profile', form=form)

def leaderboard():
    users = User.query.order_by(User.points.desc()).limit(10).all()
    return render_template('leaderboard.html', users=users)
