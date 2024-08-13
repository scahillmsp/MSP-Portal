import pandas as pd
from werkzeug.security import generate_password_hash
from app import app, db, User  # Ensure app, db, and User are imported correctly

def load_users_from_excel(file_path='users.xlsx', sheet_name='Users'):
    # Read the Excel file
    users_df = pd.read_excel(file_path, sheet_name=sheet_name)

    with app.app_context():
        for index, row in users_df.iterrows():
            username = row['username']
            password = row['password']
            name = row['name']
            
            # Check if the user already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                print(f"User '{username}' already exists. Skipping...")
                continue

            # Hash the password
            hashed_password = generate_password_hash(password)

            # Create and add the new user with the name
            new_user = User(username=username, password=hashed_password, name=name)
            db.session.add(new_user)

        # Commit all new users to the database
        db.session.commit()
        print("Users added successfully from Excel.")

if __name__ == '__main__':
    load_users_from_excel()
