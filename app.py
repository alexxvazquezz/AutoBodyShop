from flask import Flask, render_template
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from models import db
from routes import bp

app = Flask(__name__)

def create_app():
    app.config.from_object('config.Config')

    db.init_app(app)
    app.register_blueprint(bp, url_prefix='/api')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'api.login'

    jwt = JWTManager(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    with app.app_context():
        db.create_all()

    return app

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)