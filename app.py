from flask import Flask

from routes.login import login_bp
from routes.public import public_bp

app = Flask(__name__)



app.register_blueprint(public_bp)
app.register_blueprint(login_bp)

if __name__ == '__main__':
    app.run()
