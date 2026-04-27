from flask import Blueprint
from src.controllers.sensorController import receive_sensor_data, get_sensor_readings

sensor_bp = Blueprint("sensors", __name__)

# POST /api/sensors — send sensor data fra IoT device
@sensor_bp.route("/", methods=["POST"])
def post_sensor_data():
    return receive_sensor_data()

# GET /api/sensors — hent alle sensor readings
@sensor_bp.route("/", methods=["GET"])
def get_readings():
    return get_sensor_readings()