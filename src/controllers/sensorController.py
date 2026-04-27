from flask import request, jsonify
from src.config.database import get_db

def receive_sensor_data():
    try:
        data = request.get_json()
        device_id = data["device_id"]
        sensor_type = data["sensor_type"]
        value = data["value"]
        unit = data["unit"]

        db = get_db()
        cursor = db.cursor()

        # Gem sensor reading i databasen
        cursor.execute(
            "INSERT INTO sensor_readings (device_id, sensor_type, value, unit) VALUES (%s, %s, %s, %s)",
            (device_id, sensor_type, value, unit)
        )
        db.commit()
        reading_id = cursor.lastrowid

        # Threshold check — anomaly detection
        check_threshold(cursor, db, device_id, sensor_type, value)

        cursor.close()
        db.close()

        return jsonify({"message": "Sensor data modtaget", "id": reading_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_sensor_readings():
    try:
        device_id = request.args.get("device_id")

        db = get_db()
        cursor = db.cursor(dictionary=True)

        if device_id:
            cursor.execute(
                "SELECT * FROM sensor_readings WHERE device_id = %s ORDER BY received_at DESC LIMIT 50",
                (device_id,)
            )
        else:
            cursor.execute(
                "SELECT * FROM sensor_readings ORDER BY received_at DESC LIMIT 50"
            )

        rows = cursor.fetchall()
        cursor.close()
        db.close()

        return jsonify(rows), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def check_threshold(cursor, db, device_id, sensor_type, value):
    thresholds = {
        "temperature": {"warning": 70, "critical": 90},
        "pressure":    {"warning": 80, "critical": 95},
        "vibration":   {"warning": 50, "critical": 75},
    }

    threshold = thresholds.get(sensor_type)
    if not threshold:
        return

    severity = None
    message = None

    if value >= threshold["critical"]:
        severity = "HIGH"
        message = f"KRITISK: {sensor_type} på {device_id} er {value} — over kritisk grænse ({threshold['critical']})"
    elif value >= threshold["warning"]:
        severity = "MEDIUM"
        message = f"ADVARSEL: {sensor_type} på {device_id} er {value} — over advarselgrænse ({threshold['warning']})"

    if severity:
        cursor.execute(
            """INSERT INTO alerts (device_id, sensor_type, triggered_value, threshold_value, severity, message)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (device_id, sensor_type, value, threshold["critical"], severity, message)
        )
        db.commit()