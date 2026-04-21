from flask import Flask

from routes.login import login_bp
from routes.public import public_bp
from routes.secure_routes import secure_bp
from security.auth import SECRET
import logging

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET

@app.after_request
def after_request(response):
    #ochrona przed click hijacking
    response.headers["X-Frame-Options"] = "DENY"

    #ochrona przed MIME Sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    #ochrona przed XSS w starszych przeglądarkach
    response.headers["X-XSS-Protection"] = "1; mode=block"

    #strict transport security (HTTPS)
    response.headers['Strict-Transport-Security'] = "max-age=63072000; includeSubDomains; preload"

    #Content Security Policy
    response.headers['Content-Security-Policy'] = "default-src 'self';"

    return response

logging.basicConfig(
    filename='security.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',

)

app.register_blueprint(public_bp)
app.register_blueprint(login_bp)

app.register_blueprint(secure_bp)

if __name__ == '__main__':
    app.run()
