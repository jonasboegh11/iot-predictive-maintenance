from flask import Flask
from dotenv import load_dotenv
import os

from src.routes.sensorRoutes import sensor_bp
import src.routes.alertRoutes
from src.middleware.errorHandler import register_error_handlers

load_dotenv()

app = Flask(__name__)

# Registrer routes
app.register_blueprint(sensor_bp, url_prefix="/api/sensors")
app.register_blueprint(src.routes.alertRoutes.alert_bp, url_prefix="/api/alerts")
register_error_handlers(app)

# Health check
@app.route("/api/health")
def health():
    return {"status": "OK", "message": "API is running"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(debug=True, port=port)