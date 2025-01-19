from flask import Flask
from routes.home_routes import home_bp
from routes.financial_routes import financial_bp
from routes.lead_routes import lead_bp
import services.financial_data as finantial
from apscheduler.schedulers.background import BackgroundScheduler
from services.financial_data import validate_financial_data
from services.email_service import verificar_bulk_status

app = Flask(__name__)


# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(financial_bp, url_prefix='/financial')
app.register_blueprint(lead_bp, url_prefix='/lead')

finantial.validate_financial_data()

scheduler = BackgroundScheduler()
scheduler.add_job(validate_financial_data, 'interval', days=5)
scheduler.start()

scheduler = BackgroundScheduler()
scheduler.add_job(verificar_bulk_status, 'interval', hours=4)
scheduler.start()

if __name__ == "__main__":
    app.run()
