from flask import Flask
from models import db

def reset_database(app):
    with app.app_context():
        db.drop_all()
        print("All tables dropped.")
        db.create_all()
        print("All tables created.")

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    reset_database(app)