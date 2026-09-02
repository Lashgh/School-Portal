import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from config import Config, BASE_DIR
from models import db, Student, ADMISSION_STATUSES

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'portal.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()  # creates portal.db and the students table if they don't exist yet


@app.context_processor
def inject_current_year():
    return {'current_year': datetime.utcnow().year}


def allowed_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    )


REQUIRED_FORM_FIELDS = [
    'first_name', 'middle_name', 'last_name', 'email', 'date_of_birth',
    'gender', 'phone_number', 'address', 'state_of_origin',
    'local_government', 'next_of_kin', 'jamb_score',
]


@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        missing = [f for f in REQUIRED_FORM_FIELDS if not request.form.get(f)]
        image = request.files.get('image')

        if missing or image is None or image.filename == '':
            error = "Please fill in all required fields, including the image."
            return render_template('portal_form.html', error=error), 400

        if not allowed_file(image.filename):
            error = "Image must be a PNG, JPG, JPEG, or GIF file."
            return render_template('portal_form.html', error=error), 400

        try:
            date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
            jamb_score = int(request.form['jamb_score'])
        except ValueError:
            error = "Please enter a valid date of birth and a numeric JAMB score."
            return render_template('portal_form.html', error=error), 400

        # Save the image under a unique name so two students can't overwrite each other's photo
        original_name = secure_filename(image.filename)
        unique_filename = f"{uuid.uuid4().hex}_{original_name}"
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

        student = Student(
            first_name=request.form['first_name'].strip(),
            middle_name=request.form['middle_name'].strip(),
            last_name=request.form['last_name'].strip(),
            email=request.form['email'].strip(),
            date_of_birth=date_of_birth,
            gender=request.form['gender'],
            phone_number=request.form['phone_number'].strip(),
            address=request.form['address'].strip(),
            state_of_origin=request.form['state_of_origin'],
            local_government=request.form['local_government'],
            next_of_kin=request.form['next_of_kin'].strip(),
            image_filename=unique_filename,
            jamb_score=jamb_score,
        )
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('roster'))

    return render_template('portal_form.html', error=None)


@app.route('/roster')
def roster():
    name = request.args.get('name', '').strip()
    admission_status = request.args.get('admission_status', '').strip()
    gender = request.args.get('gender', '').strip()
    jamb_score = request.args.get('jamb_score', '').strip()

    query = Student.query

    if name:
        like = f"%{name}%"
        query = query.filter(
            (Student.first_name.ilike(like))
            | (Student.middle_name.ilike(like))
            | (Student.last_name.ilike(like))
        )
    if admission_status:
        query = query.filter(Student.admission_status == admission_status)
    if gender:
        query = query.filter(Student.gender == gender)
    if jamb_score:
        try:
            query = query.filter(Student.jamb_score == int(jamb_score))
        except ValueError:
            pass  # non-numeric jamb_score search term is just ignored

    students = query.order_by(Student.id).all()

    filters = {
        'name': name,
        'admission_status': admission_status,
        'gender': gender,
        'jamb_score': jamb_score,
    }

    return render_template(
        'roster.html', students=students, filters=filters, statuses=ADMISSION_STATUSES
    )


@app.route('/students/<int:student_id>')
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('details.html', student=student, statuses=ADMISSION_STATUSES)


@app.route('/students/<int:student_id>/status', methods=['POST'])
def update_status(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.get_json(silent=True) or {}
    new_status = data.get('status', '').strip()

    if new_status not in ADMISSION_STATUSES:
        return jsonify({'error': 'Invalid status'}), 400

    student.admission_status = new_status
    db.session.commit()

    return jsonify({'status': student.admission_status})


if __name__ == '__main__':
    app.run(debug=True)
