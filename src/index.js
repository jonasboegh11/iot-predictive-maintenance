require("dotenv").config();
const express = require("express");
const cors = require("cors");
const morgan = require("morgan");

const sensorRoutes = require("./routes/sensorRoutes");
const alertRoutes = require("./routes/alertRoutes");
const errorHandler = require("./middleware/errorHandler");

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(morgan("dev"));
app.use(express.json());

// Routes
app.use("/api/sensors", sensorRoutes);
app.use("/api/alerts", alertRoutes);

// Health check
app.get("/api/health", (req, res) => {
  res.json({ status: "OK", message: "API is running" });
});

// Error handler
app.use(errorHandler);

app.listen(PORT, () => {
  console.log(`Server kører på port ${PORT}`);
});