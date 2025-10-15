from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Contact {self.name}>'

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    # Sample projects data
    project_list = [
        {
            'title': 'Student Database Manager',
            'description': 'A Flask application with SQLAlchemy for managing student records with CRUD operations.',
            'technologies': ['Python', 'Flask', 'SQLAlchemy', 'SQLite'],
            'image': 'project1.jpg'
        },
        {
            'title': 'Portfolio Website',
            'description': 'A responsive portfolio website built with Flask and Bootstrap showcasing my projects and skills.',
            'technologies': ['Python', 'Flask', 'Bootstrap', 'HTML/CSS'],
            'image': 'project2.jpg'
        },
        {
            'title': 'Task Management API',
            'description': 'RESTful API for task management with user authentication and database integration.',
            'technologies': ['Python', 'Flask', 'REST API', 'JWT'],
            'image': 'project3.jpg'
        }
    ]
    return render_template('projects.html', projects=project_list)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if name and email and message:
            try:
                new_contact = Contact(
                    name=name,
                    email=email,
                    message=message
                )
                db.session.add(new_contact)
                db.session.commit()
                flash('Thank you for your message! I will get back to you soon.', 'success')
                return redirect(url_for('contact'))
            except Exception as e:
                flash(f'Error submitting form: {str(e)}', 'error')
        else:
            flash('All fields are required!', 'error')
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
