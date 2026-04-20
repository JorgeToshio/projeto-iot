-- View 1: Média de temperatura por dispositivo
CREATE VIEW avg_temp_por_dispositivo AS
SELECT device_id, AVG(temp) as avg_temp 
FROM temperature_readings 
GROUP BY device_id;

-- View 2: Contagem de leituras por data
CREATE VIEW leituras_por_dia AS
SELECT noted_date::date as data, COUNT(*) as contagem
FROM temperature_readings
GROUP BY noted_date::date;