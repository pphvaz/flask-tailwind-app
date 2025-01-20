from flask import Flask
from routes.home_routes import home_bp
from routes.financial_routes import financial_bp
from routes.lead_routes import lead_bp
import services.financial_data as finantial
from apscheduler.schedulers.background import BackgroundScheduler
from services.financial_data import validate_financial_data
from services.email_service import verificar_bulk_status
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
from flask_talisman import Talisman
import os

load_dotenv()

# Configure logging
handler = RotatingFileHandler('error.log', maxBytes=100000, backupCount=3)
handler.setLevel(logging.ERROR)
logging.basicConfig(level=logging.ERROR, handlers=[handler])

# Initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('CSRF_SECRET_KEY')
app.config['PREFERRED_URL_SCHEME'] = 'https'

# Use Talisman for enforcing HTTPS and adding security headers
Talisman(app, content_security_policy=None)

# CSRF protection
csrf = CSRFProtect(app)
print(CSRFProtect)

# Set Content Security Policy (CSP)
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "  # Restrict other resources to your domain
        "script-src 'self' https://www.googletagmanager.com https://www.google-analytics.com https://www.google.com https://cdn.jsdelivr.net https://www.gstatic.com; "  # Allow reCAPTCHA and SweetAlert2 CDN
        "style-src 'self' 'unsafe-inline'; "  # Allow inline styles
        "img-src 'self' data: https://www.google-analytics.com; "  # Allow images and data URIs
        "connect-src 'self' https://api.mailersend.com https://www.google-analytics.com; "  # Allow MailerSend and API connections
        "frame-src 'self' https://www.google.com;"  # Allow framing from Google (for reCAPTCHA)
    )
    return response

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(financial_bp, url_prefix='/financial')
app.register_blueprint(lead_bp, url_prefix='/lead')

finantial.validate_financial_data()

scheduler = BackgroundScheduler()
scheduler.add_job(validate_financial_data, 'interval', days=5)
scheduler.add_job(verificar_bulk_status, 'interval', hours=4)
scheduler.start()

if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'))
    # app.run(debug=False)
