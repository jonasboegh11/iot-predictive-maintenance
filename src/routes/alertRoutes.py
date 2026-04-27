from flask import Blueprint
from src.controllers.alertController import get_alerts, resolve_alert

alert_bp = Blueprint("alerts", __name__)

# GET /api/alerts — hent alle alerts
@alert_bp.route("/", methods=["GET"])
def get_all_alerts():
    return get_alerts()

# PUT /api/alerts/<id>/resolve — marker alert som løst
@alert_bp.route("/<int:id>/resolve", methods=["PUT"])
def resolve_one_alert(id):
    return resolve_alert(id)