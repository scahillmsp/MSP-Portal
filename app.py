import os
import webbrowser
from flask import Flask, render_template, redirect, url_for, flash, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Use a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model with username and password fields
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Determine the base directory of the script
basedir = os.path.abspath(os.path.dirname(__file__))

# Load data from the Excel file using a relative path
excel_file = os.path.join(basedir, 'parts_data.xlsx')
parts_df = pd.read_excel(excel_file, sheet_name='Parts')

@app.route('/')
def index():
    # Check if user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Fetch the user from the database
        user = User.query.filter_by(username=username).first()
        # Check user credentials using hashed password verification
        if user and check_password_hash(user.password, password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/api/dropdowns', methods=['GET'])
def get_dropdowns():
    try:
        makes = parts_df['Make'].dropna().unique()
        models = parts_df['Model'].dropna().unique()
        versions = parts_df['Version'].dropna().unique()
        categories = parts_df['Category'].dropna().unique()

        data = {
            'makes': [{'id': idx, 'name': make} for idx, make in enumerate(makes)],
            'models': [{'id': idx, 'name': model} for idx, model in enumerate(models)],
            'versions': [{'id': idx, 'name': version} for idx, version in enumerate(versions)],
            'categories': [{'id': idx, 'name': category} for idx, category in enumerate(categories)]
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    make = request.args.get('make')
    if make:
        models = parts_df[parts_df['Make'] == make]['Model'].dropna().unique()
        data = {'models': [{'id': idx, 'name': model} for idx, model in enumerate(models)]}
        return jsonify(data)
    return jsonify({'models': []})

@app.route('/api/versions', methods=['GET'])
def get_versions():
    model = request.args.get('model')
    if model:
        versions = parts_df[parts_df['Model'] == model]['Version'].dropna().unique()
        data = {'versions': [{'id': idx, 'name': version} for idx, version in enumerate(versions)]}
        return jsonify(data)
    return jsonify({'versions': []})

@app.route('/api/categories', methods=['GET'])
def get_categories():
    version = request.args.get('version')
    if version:
        categories = parts_df[parts_df['Version'] == version]['Category'].dropna().unique()
        data = {'categories': [{'id': idx, 'name': category} for idx, category in enumerate(categories)]}
        return jsonify(data)
    return jsonify({'categories': []})

@app.route('/api/parts', methods=['GET'])
def get_parts():
    make = request.args.get('make')
    model = request.args.get('model')
    version = request.args.get('version')
    category = request.args.get('category')

    query = parts_df
    if make:
        query = query[query['Make'] == make]
    if model:
        query = query[query['Model'] == model]
    if version:
        query = query[query['Version'] == version]
    if category:
        query = query[query['Category'] == category]

    parts = query[['Part', 'Part Number']].drop_duplicates().to_dict(orient='records')
    return jsonify(parts)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=False, host='0.0.0.0', port=port)
