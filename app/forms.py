from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField, FloatField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, Optional
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('student', 'Student'), ('alumni', 'Alumni'), ('faculty', 'Faculty')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if self.role.data == 'student':
            import re
            pattern = r'^[sS][nN][gG][a-zA-Z0-9]+@sngce\.ac\.in$'
            if not re.match(pattern, email.data):
                raise ValidationError("Student emails must be of the form sngxxxxxxx@sngce.ac.in (e.g. SNG23CS010@sngce.ac.in)")
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class JobPostForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    job_type = SelectField('Job Type', choices=[('Internship', 'Internship'), ('Full-time', 'Full-time'), ('Part-time', 'Part-time')], validators=[DataRequired()])
    target_year = SelectField('Target Year', choices=[('All', 'All Students'), ('1st Year', '1st Year'), ('2nd Year', '2nd Year'), ('3rd Year', '3rd Year'), ('4th Year', '4th Year')], validators=[DataRequired()])
    apply_link = StringField('Application Link', validators=[DataRequired()])
    application_deadline = DateField('Application Deadline', validators=[Optional()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post Job')

class AlumniProfileForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    enrollment_year = IntegerField('Enrollment Year', validators=[Optional(), NumberRange(min=1950, max=3000)])
    graduation_year = IntegerField('Graduation Year', validators=[Optional(), NumberRange(min=1950, max=3000)])
    degree = StringField('Degree', validators=[Optional()])
    department = SelectField('Department', choices=[
        ('CSE', 'Computer Science'),
        ('ECE', 'Electronics & Communication'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('EEE', 'Electrical & Electronics'),
        ('AS', 'Applied Science'),
        ('MCA', 'Master of Computer Applications'),
        ('MBA', 'Master of Business Administration'),
        ('Other', 'Other (Enter Below)')
    ], validators=[Optional()])
    current_company = StringField('Current Company')
    current_position = StringField('Current Position')
    linkedin_url = StringField('LinkedIn URL')
    resume = FileField('Upload Resume (PDF)', validators=[FileAllowed(['pdf'])])
    submit = SubmitField('Update Profile')

class StudentProfileForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    enrollment_year = IntegerField('Enrollment Year', validators=[Optional(), NumberRange(min=1980, max=3000)])
    expected_graduation_year = IntegerField('Expected Graduation Year', validators=[Optional(), NumberRange(min=1980, max=3000)])
    department = StringField('Department', validators=[Optional()])
    cgpa = FloatField('CGPA', validators=[Optional()])
    submit = SubmitField('Update Profile')

class FacultyProfileForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    department = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class EventPhotoForm(FlaskForm):
    photo = FileField('Upload Photo', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    category = SelectField('Category', choices=[('event', 'Community Event'), ('job_poster', 'Job Poster/Flyer')], validators=[DataRequired()])
    event_name = StringField('Title/Event Name', validators=[DataRequired(), Length(max=100)])
    caption = TextAreaField('Description/Caption', validators=[Length(max=200)])
    submit = SubmitField('Upload to Gallery')

class JobPosterForm(FlaskForm):
    photo = FileField('Upload Job Poster', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    title = StringField('Job Title/Topic', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=200)])
    submit = SubmitField('Post to Gallery')

