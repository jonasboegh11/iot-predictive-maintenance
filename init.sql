-- ============================================================
-- IoT Predictive Maintenance - Database initialisering
-- ============================================================

CREATE DATABASE IF NOT EXISTS iot_maintenance;
USE iot_maintenance;

-- ------------------------------------------------------------
-- Tabel: sensor_readings
-- Gemmer rå sensordata fra IoT-enheder
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sensor_readings (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    device_id   VARCHAR(100)   NOT NULL,
    sensor_type VARCHAR(50)    NOT NULL,
    value       DECIMAL(10, 2) NOT NULL,
    unit        VARCHAR(20)    NOT NULL,
    received_at DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_device_id   (device_id),
    INDEX idx_sensor_type (sensor_type),
    INDEX idx_received_at (received_at)
);

-- ------------------------------------------------------------
-- Tabel: alerts
-- Gemmer automatisk genererede alarmer ved threshold-overskridelse
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS alerts (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    device_id       VARCHAR(100)   NOT NULL,
    sensor_type     VARCHAR(50)    NOT NULL,
    triggered_value DECIMAL(10, 2) NOT NULL,
    threshold_value DECIMAL(10, 2) NOT NULL,
    severity        ENUM('MEDIUM', 'HIGH') NOT NULL,
    message         TEXT           NOT NULL,
    resolved        BOOLEAN        NOT NULL DEFAULT FALSE,
    resolved_at     DATETIME                DEFAULT NULL,
    created_at      DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_device_id  (device_id),
    INDEX idx_severity   (severity),
    INDEX idx_resolved   (resolved),
    INDEX idx_created_at (created_at)
);