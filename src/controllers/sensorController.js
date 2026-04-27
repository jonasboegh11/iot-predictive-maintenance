const db = require("../config/database");

// Modtag sensor data fra IoT device
const receiveSensorData = async (req, res, next) => {
  try {
    const { device_id, sensor_type, value, unit } = req.body;

    // Gem sensor reading i databasen
    const [result] = await db.query(
      `INSERT INTO sensor_readings (device_id, sensor_type, value, unit) 
       VALUES (?, ?, ?, ?)`,
      [device_id, sensor_type, value, unit]
    );

    // Threshold check — anomaly detection
    await checkThreshold(device_id, sensor_type, value);

    res.status(201).json({
      message: "Sensor data modtaget",
      id: result.insertId,
    });
  } catch (err) {
    next(err);
  }
};

// Hent alle sensor readings
const getSensorReadings = async (req, res, next) => {
  try {
    const { device_id } = req.query;

    let query = "SELECT * FROM sensor_readings";
    let params = [];

    if (device_id) {
      query += " WHERE device_id = ?";
      params.push(device_id);
    }

    query += " ORDER BY received_at DESC LIMIT 50";

    const [rows] = await db.query(query, params);
    res.json(rows);
  } catch (err) {
    next(err);
  }
};

// Threshold logik — hjerte af predictive maintenance
const checkThreshold = async (device_id, sensor_type, value) => {
  const thresholds = {
    temperature: { warning: 70, critical: 90 },
    pressure: { warning: 80, critical: 95 },
    vibration: { warning: 50, critical: 75 },
  };

  const threshold = thresholds[sensor_type];
  if (!threshold) return;

  let severity = null;
  let message = null;

  if (value >= threshold.critical) {
    severity = "HIGH";
    message = `KRITISK: ${sensor_type} på ${device_id} er ${value} — over kritisk grænse (${threshold.critical})`;
  } else if (value >= threshold.warning) {
    severity = "MEDIUM";
    message = `ADVARSEL: ${sensor_type} på ${device_id} er ${value} — over advarselgrænse (${threshold.warning})`;
  }

  if (severity) {
    await db.query(
      `INSERT INTO alerts (device_id, sensor_type, triggered_value, threshold_value, severity, message)
       VALUES (?, ?, ?, ?, ?, ?)`,
      [device_id, sensor_type, value, threshold.critical, severity, message]
    );
  }
};

module.exports = { receiveSensorData, getSensorReadings };