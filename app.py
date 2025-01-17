from flask import Flask
from routes.home_routes import home_bp
from routes.financial_routes import financial_bp
from routes.lead_routes import lead_bp

app = Flask(__name__)
app.config.from_object('config.Config')

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(financial_bp, url_prefix='/financial')
app.register_blueprint(lead_bp, url_prefix='/lead')

if __name__ == "__main__":
    app.run()