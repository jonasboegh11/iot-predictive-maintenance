from flask import request, jsonify
from src.config.database import get_db

def get_alerts():
    try:
        device_id = request.args.get("device_id")
        resolved = request.args.get("resolved")

        db = get_db()
        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM alerts WHERE 1=1"
        params = []

        if device_id:
            query += " AND device_id = %s"
            params.append(device_id)

        if resolved is not None:
            query += " AND resolved = %s"
            params.append(1 if resolved == "true" else 0)

        query += " ORDER BY created_at DESC LIMIT 50"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        db.close()

        return jsonify(rows), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def resolve_alert(id):
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "UPDATE alerts SET resolved = true, resolved_at = NOW() WHERE id = %s",
            (id,)
        )
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Alert ikke fundet"}), 404

        cursor.close()
        db.close()

        return jsonify({"message": f"Alert {id} er markeret som løst"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500