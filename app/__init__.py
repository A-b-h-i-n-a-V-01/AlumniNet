import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload directory exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Register Routes
    from app import routes
    app.add_url_rule('/', 'index', routes.index)
    app.add_url_rule('/register', 'register', routes.register, methods=['GET', 'POST'])
    app.add_url_rule('/login', 'login', routes.login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', routes.logout)
    app.add_url_rule('/dashboard', 'dashboard', routes.dashboard)
    app.add_url_rule('/jobs', 'jobs', routes.jobs)
    app.add_url_rule('/job/new', 'new_job', routes.new_job, methods=['GET', 'POST'])
    app.add_url_rule('/approve/job/<int:job_id>', 'approve_job', routes.approve_job)
    app.add_url_rule('/approve/alumni/<int:profile_id>', 'approve_alumni', routes.approve_alumni)
    app.add_url_rule('/profile', 'profile', routes.profile, methods=['GET', 'POST'])
    app.add_url_rule('/leaderboard', 'leaderboard', routes.leaderboard)

    # Create tables within application context if they don't exist
    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from app import models
        db.create_all()

    return app
