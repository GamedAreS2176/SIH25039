-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS h3;

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'citizen' CHECK (role IN ('citizen', 'analyst', 'official')),
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create hazard reports table
CREATE TABLE hazard_reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    hazard_type VARCHAR(50) NOT NULL CHECK (hazard_type IN (
        'tsunami', 'storm_surge', 'high_waves', 'swell_surge', 
        'coastal_current', 'flooding', 'abnormal_tide', 'other'
    )),
    severity VARCHAR(20) DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    location GEOMETRY(POINT, 4326) NOT NULL,
    h3_index VARCHAR(20), -- H3 spatial index for clustering
    media_urls TEXT[], -- Array of media file URLs
    is_verified BOOLEAN DEFAULT FALSE,
    verified_by INTEGER REFERENCES users(id),
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create social media posts table
CREATE TABLE social_media_posts (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(20) NOT NULL CHECK (platform IN ('twitter', 'facebook', 'youtube')),
    post_id VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(100),
    location GEOMETRY(POINT, 4326),
    hazard_keywords TEXT[],
    sentiment_score FLOAT,
    hazard_probability FLOAT,
    engagement_metrics JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create hotspots table for dynamic clustering
CREATE TABLE hotspots (
    id SERIAL PRIMARY KEY,
    center_location GEOMETRY(POINT, 4326) NOT NULL,
    radius_meters INTEGER NOT NULL,
    report_count INTEGER DEFAULT 0,
    severity_level VARCHAR(20) DEFAULT 'medium',
    hazard_types TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- Create alerts table for INCOIS integration
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    alert_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    affected_area GEOMETRY(POLYGON, 4326),
    severity VARCHAR(20) NOT NULL,
    source VARCHAR(50) DEFAULT 'incois',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- Create user alerts junction table
CREATE TABLE user_alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    alert_id INTEGER REFERENCES alerts(id),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_hazard_reports_location ON hazard_reports USING GIST (location);
CREATE INDEX idx_hazard_reports_h3_index ON hazard_reports (h3_index);
CREATE INDEX idx_hazard_reports_created_at ON hazard_reports (created_at);
CREATE INDEX idx_hazard_reports_hazard_type ON hazard_reports (hazard_type);

CREATE INDEX idx_social_media_location ON social_media_posts USING GIST (location);
CREATE INDEX idx_social_media_platform ON social_media_posts (platform);
CREATE INDEX idx_social_media_created_at ON social_media_posts (created_at);

CREATE INDEX idx_hotspots_location ON hotspots USING GIST (center_location);
CREATE INDEX idx_hotspots_expires_at ON hotspots (expires_at);

CREATE INDEX idx_alerts_affected_area ON alerts USING GIST (affected_area);
CREATE INDEX idx_alerts_is_active ON alerts (is_active);

-- Function to update H3 index when location changes
CREATE OR REPLACE FUNCTION update_h3_index()
RETURNS TRIGGER AS $$
BEGIN
    NEW.h3_index = h3_lat_lng_to_cell(ST_Y(NEW.location), ST_X(NEW.location), 8);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update H3 index
CREATE TRIGGER trigger_update_h3_index
    BEFORE INSERT OR UPDATE ON hazard_reports
    FOR EACH ROW
    EXECUTE FUNCTION update_h3_index();

-- Function to create hotspots based on report density
CREATE OR REPLACE FUNCTION generate_hotspots()
RETURNS VOID AS $$
DECLARE
    report_record RECORD;
    hotspot_radius INTEGER := 5000; -- 5km radius
BEGIN
    -- Clear existing hotspots
    DELETE FROM hotspots WHERE expires_at < NOW();
    
    -- Generate new hotspots based on report density
    INSERT INTO hotspots (center_location, radius_meters, report_count, severity_level, hazard_types)
    SELECT 
        ST_Centroid(ST_Collect(location)) as center_location,
        hotspot_radius,
        COUNT(*) as report_count,
        CASE 
            WHEN COUNT(*) >= 10 THEN 'critical'
            WHEN COUNT(*) >= 5 THEN 'high'
            WHEN COUNT(*) >= 3 THEN 'medium'
            ELSE 'low'
        END as severity_level,
        ARRAY_AGG(DISTINCT hazard_type) as hazard_types
    FROM hazard_reports 
    WHERE created_at >= NOW() - INTERVAL '24 hours'
    GROUP BY h3_index
    HAVING COUNT(*) >= 2;
END;
$$ LANGUAGE plpgsql;

-- Sample data for testing
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@datadolphins.in', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2K', 'official'),
('analyst1', 'analyst@datadolphins.in', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2K', 'analyst'),
('citizen1', 'citizen@datadolphins.in', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2K', 'citizen');

-- Sample hazard reports
INSERT INTO hazard_reports (user_id, title, description, hazard_type, severity, location) VALUES
(3, 'High waves observed at Marina Beach', 'Unusually high waves hitting the shore with strong currents', 'high_waves', 'high', ST_SetSRID(ST_MakePoint(80.2707, 13.0827), 4326)),
(3, 'Coastal flooding in Chennai', 'Water levels rising rapidly near the beach area', 'flooding', 'critical', ST_SetSRID(ST_MakePoint(80.2206, 13.0475), 4326)),
(3, 'Abnormal tide patterns', 'Tide levels much higher than normal for this time', 'abnormal_tide', 'medium', ST_SetSRID(ST_MakePoint(80.2907, 13.1027), 4326));