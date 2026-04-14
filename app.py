from flask import Flask

from routes.login import login_bp
from routes.public import public_bp
from routes.secure_routes import secure_bp
from security.auth import SECRET

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET



app.register_blueprint(public_bp)
app.register_blueprint(login_bp)

app.register_blueprint(secure_bp)

if __name__ == '__main__':
    app.run()
