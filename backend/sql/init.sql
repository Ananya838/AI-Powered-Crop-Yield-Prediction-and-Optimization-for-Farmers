CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(120) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    language VARCHAR(20) NOT NULL DEFAULT 'en',
    hashed_password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS farms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    farm_name VARCHAR(120) NOT NULL,
    district VARCHAR(80) NOT NULL,
    village VARCHAR(80) NOT NULL,
    area_hectare FLOAT NOT NULL,
    irrigation_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS soil_reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    farm_id INT NOT NULL,
    nitrogen FLOAT NOT NULL,
    phosphorus FLOAT NOT NULL,
    potassium FLOAT NOT NULL,
    ph FLOAT NOT NULL,
    organic_carbon FLOAT,
    moisture FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id)
);

CREATE TABLE IF NOT EXISTS weather_cache (
    id INT PRIMARY KEY AUTO_INCREMENT,
    district VARCHAR(80) NOT NULL,
    season VARCHAR(30) NOT NULL,
    avg_rainfall_mm FLOAT NOT NULL,
    avg_temperature_c FLOAT NOT NULL,
    raw_payload TEXT,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS yield_predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    farm_id INT,
    crop VARCHAR(80) NOT NULL,
    season VARCHAR(30) NOT NULL,
    predicted_yield FLOAT NOT NULL,
    confidence_score FLOAT NOT NULL,
    suggested_crop VARCHAR(80),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (farm_id) REFERENCES farms(id)
);

CREATE TABLE IF NOT EXISTS pest_alerts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    district VARCHAR(80) NOT NULL,
    crop VARCHAR(80) NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    risk_score FLOAT NOT NULL,
    advisory TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    farm_id INT,
    irrigation_schedule TEXT NOT NULL,
    fertilizer_dosage TEXT NOT NULL,
    sowing_date VARCHAR(30) NOT NULL,
    harvest_window VARCHAR(30) NOT NULL,
    rotation_advice TEXT,
    expected_gain_percent FLOAT NOT NULL DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (farm_id) REFERENCES farms(id)
);

CREATE TABLE IF NOT EXISTS crop_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    district VARCHAR(80) NOT NULL,
    crop VARCHAR(80) NOT NULL,
    season VARCHAR(30) NOT NULL,
    yield_per_hectare FLOAT NOT NULL,
    year INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS district_stats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    district VARCHAR(80) UNIQUE NOT NULL,
    avg_productivity FLOAT NOT NULL,
    adoption_rate FLOAT NOT NULL,
    failure_alert_count INT NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
