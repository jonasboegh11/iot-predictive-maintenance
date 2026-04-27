const express = require("express");
const router = express.Router();
const { receiveSensorData, getSensorReadings } = require("../controllers/sensorController");

// POST /api/sensors — send sensor data fra IoT device
router.post("/", receiveSensorData);

// GET /api/sensors — hent alle sensor readings
router.get("/", getSensorReadings);

module.exports = router;