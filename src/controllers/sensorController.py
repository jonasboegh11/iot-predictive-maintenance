from flask import request, jsonify
from src.config.database import get_db


def check_threshold(cursor, db, device_id, sensor_type, value):
    try:
        thresholds = {
            "temperature":  {"warning": 70,   "critical": 90},
            "rpm":          {"warning": 1600, "critical": 1800},
            "power_output": {"warning": 1800, "critical": 2100},
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

    except Exception as e:
        print(f"DEBUG check_threshold fejl: {e}")


def check_trend(cursor, db, device_id, sensor_type):
    try:
        thresholds = {
            "temperature":  {"normal": 50,   "warning": 70,   "critical": 90},
            "rpm":          {"normal": 1200, "warning": 1600, "critical": 1800},
            "power_output": {"normal": 1500, "warning": 1800, "critical": 2100},
        }

        threshold = thresholds.get(sensor_type)
        if not threshold:
            return

        trend_cursor = db.cursor()
        trend_cursor.execute(
            """SELECT value FROM sensor_readings 
               WHERE device_id = %s AND sensor_type = %s 
               ORDER BY id DESC LIMIT 5""",
            (device_id, sensor_type)
        )
        rows = trend_cursor.fetchall()

        if len(rows) < 5:
            return

        values = [float(row[0]) for row in reversed(rows)]

        # Kun relevant hvis seneste værdi er i pre-warning zonen
        if not (threshold["normal"] <= values[-1] < threshold["warning"]):
            return

        stiger_konsekvent = all(values[i] < values[i+1] for i in range(len(values)-1))

        if stiger_konsekvent:
            stigning = values[-1] - values[0]
            message = (
                f"TREND: {sensor_type} på {device_id} har steget {stigning:.1f} "
                f"over de sidste 5 målinger ({values[0]} → {values[-1]}). "
                f"Mulig fejludvikling."
            )
            trend_cursor.execute(
                """INSERT INTO alerts 
                   (device_id, sensor_type, triggered_value, threshold_value, severity, message)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (device_id, sensor_type, values[-1], threshold["warning"], "MEDIUM", message)
            )
            db.commit()

        trend_cursor.close()

    except Exception as e:
        print(f"DEBUG check_trend fejl: {e}")


def receive_sensor_data():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Ugyldigt eller tomt request body"}), 400

        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list):
            return jsonify({"error": "Ugyldigt format"}), 400

        for item in data:
            if not all(k in item for k in ["device_id", "sensor_type", "value", "unit"]):
                return jsonify({"error": "Manglende felter i et af objekterne"}), 400

        db = get_db()
        cursor = db.cursor()

        ids = []
        for item in data:
            cursor.execute(
                "INSERT INTO sensor_readings (device_id, sensor_type, value, unit) VALUES (%s, %s, %s, %s)",
                (item["device_id"], item["sensor_type"], item["value"], item["unit"])
            )
            db.commit()
            ids.append(cursor.lastrowid)
            check_threshold(cursor, db, item["device_id"], item["sensor_type"], item["value"])

        checked = set()
        for item in data:
            key = (item["device_id"], item["sensor_type"])
            if key not in checked:
                check_trend(cursor, db, item["device_id"], item["sensor_type"])
                checked.add(key)

        cursor.close()
        db.close()

        return jsonify({"message": f"{len(ids)} sensor readings modtaget", "ids": ids}), 201

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