const express = require("express");
const router = express.Router();
const { getAlerts, resolveAlert } = require("../controllers/alertController");

// GET /api/alerts — hent alle alerts
router.get("/", getAlerts);

// PUT /api/alerts/:id/resolve — marker alert som løst
router.put("/:id/resolve", resolveAlert);

module.exports = router;