# from src.db import db
# from flask import Blueprint, flash, render_template, request, redirect, url_for
# from src.Models.User import User
# from flask_bcrypt import Bcrypt

# register_bp = Blueprint('register', __name__)
# bcrypt = Bcrypt()

# @register_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
 
#         password = request.form['password']
#         if not username or not email or not password:
#             flash('Please complete all fields', 'error')
#         elif User.query.filter_by(username=username).first():
#             flash('Username already exists', 'error')
#         elif User.query.filter_by(email=email).first():
#             flash('Email already registered', 'error') 

#         else:
            
#                 hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#                 new_user = User(username=username, email=email, password=hashed_password)
#                 db.session.add(new_user)
#                 db.session.commit()
#                 flash('Registration successful! Please log in.', 'success')
#                 return redirect(url_for('login.login'))

#     return render_template('web/auth/register.html', form_action='')




from src.db import db
from flask import Blueprint, flash, render_template, request, redirect, url_for
from src.Models.User import User
from flask_bcrypt import Bcrypt
import os # Import os module for path manipulation
from werkzeug.utils import secure_filename # Import secure_filename for secure file naming

register_bp = Blueprint('register', __name__)
bcrypt = Bcrypt()

# Configuration for file uploads
# IMPORTANT: Make sure this directory exists in your project, e.g., src/static/uploads
UPLOAD_FOLDER = 'src/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # Allowed image extensions

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        profile_picture = None # Initialize profile_picture to None

        # --- NEW: Handle file upload for profile picture ---
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                profile_picture = filename # Store only the filename in the database
            elif file.filename != '': # If a file was selected but it's not allowed
                flash('Invalid file type for profile picture. Allowed types: png, jpg, jpeg, gif.', 'error')
                # It might be good to render the template again with the old input data here
                # but for simplicity, we proceed and let the other validations catch if needed.
                return render_template('web/auth/register.html', form_action='', username=username, email=email)
        # --- END NEW ---

        # Your existing validation logic
        if not username or not email or not password:
            flash('Please complete all fields', 'error')
        elif User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            # Pass the profile_picture filename to the User constructor
            new_user = User(username=username, email=email, password=hashed_password, profile_picture=profile_picture)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login.login')) # Redirect after successful registration

    # Render the registration form for GET requests or if validation fails
    return render_template('web/auth/register.html', form_action='')