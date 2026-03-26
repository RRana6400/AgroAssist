from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone, UTC
from sqlalchemy import text
from sqlalchemy import update
import uuid



# ----------------- CONFIG -----------------
app = Flask(__name__)
app.secret_key = 'RR'   

# Database connection (⚠️ avoid root user with no password!)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3307/farmers'
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):                  # This will help to retrieve the user by id
    return User.query.get(int(user_id))


# ----------------- MODELS -----------------
# class Test(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(250), nullable = False)  

def get_ist():
    # Manual offset: UTC + 5 hours 30 minutes
    ist_offset = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist_offset)

class register_book(db.Model):
    record_no   = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    timestamp   = db.Column(db.DateTime, default=lambda:get_ist(), nullable=False)
    user_email  = db.Column(db.String(50), nullable=False)

    def __init__(self, description, user_email):
        self.description = description
        self.user_email  = user_email


# ----------------- ROUTES -----------------
@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if password != confirm_password :
            return render_template('register.html', error = "Passwords do not match")

        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('register.html', error = "Email already exists")

        hashed_password = generate_password_hash(password)
        newuser = User(username=username, email=email, password=hashed_password)
        db.session.add(newuser)
        db.session.commit()
        # flash("Signup Successful! Please Login", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        choice = request.form.get("username-email-choice")
        password = request.form.get('password')
        
        if choice == "Username":
            username = request.form.get('username-or-email')
            user = User.query.filter_by(username=username).first()

        else:
            email = request.form.get('username-or-email')
            user = User.query.filter_by(email=email).first()
        

        if user and check_password_hash(user.password, password):
            login_user(user)
            # flash("Login Success", "primary")
            return redirect(url_for('index'))
        else:
            # flash("Invalid Credentials", "danger")
            return render_template('login.html')
    return render_template('login.html')

@app.route("/home")
@login_required
def index():
    return  render_template('home.html')

@app.route("/weather")
@login_required
def weather():
    return  render_template("weather.html")
    

@app.route("/record_management")
@login_required
def record():
    all_data = db.session.execute(db.select(register_book).where(register_book.user_email == current_user.email)).scalars().all()
    
    return  render_template("record_manage.html", records=all_data)
    
@app.route("/mandi")
@login_required
def mandi():
    return  render_template("mandi.html")

@app.route("/calender")
@login_required
def calender():
    return  render_template("calender.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # flash("Logout Successful", "info")
    return redirect(url_for('login'))


@app.route('/add_desc', methods=['POST', 'GET'] )
def add_desc():
    if request.method == "POST":
        input_desc = request.form.get('input-desc')
        if(input_desc == ""):
            flash("Please, Enter some description to add...", "info")
        else:
            new_desc = register_book(description = input_desc, user_email= current_user.email)
            db.session.add(new_desc)
            db.session.execute(text("ALTER TABLE register_book AUTO_INCREMENT = 1"))
            db.session.commit()
            flash("Your description is added successfully...", "success")
        return redirect(url_for('record'))
    
    
@app.route('/alter_record', methods=['POST', 'GET'] )
def alter_record():
    if request.method == "POST":
        record_no = request.form.get('record_no')
        btn = request.form.get('alter_record')
        if(btn == 'update'):
            new_desc = request.form.get('new_desc')
            record_to_be_updated = register_book.query.get(record_no)
            record_to_be_updated.description = new_desc
            record_to_be_updated.timestamp = get_ist()
            db.session.commit()
            flash("Your description is updated successfully...", "info")
        elif(btn == 'delete'):
            record_to_be_deleted = register_book.query.get(record_no)
            db.session.delete(record_to_be_deleted)
            db.session.commit()
                    
            flash(f"Record has been deleted successfully...", "error")
        return redirect(url_for('record'))
    




if __name__ == '__main__':
    with app.app_context():  # Needed for DB operations
        db.create_all() 
    app.run(debug=True)
