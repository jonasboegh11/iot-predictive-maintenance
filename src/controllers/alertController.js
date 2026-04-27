const db = require("../config/database");

// Hent alle alerts
const getAlerts = async (req, res, next) => {
  try {
    const { device_id, resolved } = req.query;

    let query = "SELECT * FROM alerts WHERE 1=1";
    let params = [];

    if (device_id) {
      query += " AND device_id = ?";
      params.push(device_id);
    }

    if (resolved !== undefined) {
      query += " AND resolved = ?";
      params.push(resolved === "true" ? 1 : 0);
    }

    query += " ORDER BY created_at DESC LIMIT 50";

    const [rows] = await db.query(query, params);
    res.json(rows);
  } catch (err) {
    next(err);
  }
};

// Marker en alert som løst
const resolveAlert = async (req, res, next) => {
  try {
    const { id } = req.params;

    const [result] = await db.query(
      `UPDATE alerts 
       SET resolved = true, resolved_at = NOW() 
       WHERE id = ?`,
      [id]
    );

    if (result.affectedRows === 0) {
      return res.status(404).json({ error: "Alert ikke fundet" });
    }

    res.json({ message: `Alert ${id} er markeret som løst` });
  } catch (err) {
    next(err);
  }
};

module.exports = { getAlerts, resolveAlert };