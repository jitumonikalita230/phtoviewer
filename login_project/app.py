from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Mock database of users
users = {"admin": "password123", "user": "mypassword"}

# Directory for storing uploaded photos
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Check if the uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/log", methods=["POST"])
def log():
    role = request.form.get("role")
    if role == "admin":
        return redirect(url_for("admin_login"))
    elif role == "viewer":
        return redirect(url_for("welcome_viewer", username="Viewer"))
    else:
        flash("Invalid role selected. Please try again.")
        return redirect(url_for("home"))

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            return redirect(url_for("welcome", username=username))
        else:
            flash("Invalid username or password!")
            return redirect(url_for("admin_login"))
    return render_template("login.html")

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    username = request.args.get("username", "Guest")

    if request.method == "POST":
        # Handle photo upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash("Photo uploaded successfully!")
            else:
                flash("Invalid file format. Please upload an image file.")
        # Handle photo deletion
        if 'delete_photo' in request.form:
            photo_to_delete = request.form.get('delete_photo')
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_to_delete)
            if os.path.exists(photo_path):
                os.remove(photo_path)
                flash("Photo deleted successfully!")
            else:
                flash("Photo not found!")

    # List all uploaded photos
    photos = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("welcome.html", username=username, photos=photos)

@app.route("/welcome_viewer", methods=["GET"])
def welcome_viewer():
    username = request.args.get("username", "Guest")
    # List all uploaded photos (read-only for viewer)
    photos = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("welcome_viewer.html", username=username, photos=photos)

if __name__ == "__main__":
    app.run(debug=True)





 