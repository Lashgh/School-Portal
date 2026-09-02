from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

ADMISSION_STATUSES = ['undecided', 'admitted', 'rejected']


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)

    # --- Personal Information ---
    first_name = db.Column(db.String(80), nullable=False)
    middle_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)              # Male / Female (radio)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    state_of_origin = db.Column(db.String(100), nullable=False)    # dynamic select (Nigeria state)
    local_government = db.Column(db.String(100), nullable=False)   # dynamic select, depends on state
    next_of_kin = db.Column(db.String(120), nullable=False)

    # the file itself lives in static/uploads; only its name is stored here
    image_filename = db.Column(db.String(255), nullable=False)

    # --- Academics Related Information ---
    jamb_score = db.Column(db.Integer, nullable=False)

    # --- changed asynchronously from the Details page ---
    admission_status = db.Column(db.String(20), nullable=False, default='undecided')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'
