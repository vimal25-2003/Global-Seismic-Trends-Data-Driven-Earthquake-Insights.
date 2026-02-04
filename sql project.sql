CREATE database earthquake_db;
use earthquake_db;
select count(*) from earthquake;
select * from earthquake;
select id,place,mag, time 
from earthquake order by mag desc
limit 10;
select id,place,depth_km,mag
from earthquake
order by depth_km desc
limit 10;
select id,place,depth_km,mag
from earthquake
where depth_km<50 and mag>7.5;
SELECT
    CASE
        WHEN country IN ('japan', 'china', 'india', 'indonesia') THEN 'asia'
        WHEN country IN ('chile', 'peru', 'mexico') THEN 'south america'
        WHEN country IN ('united states', 'canada') THEN 'north america'
        WHEN country IN ('italy', 'greece', 'turkey') THEN 'europe'
        WHEN country IN ('new zealand') THEN 'oceania'
        ELSE 'other'
    END AS continent,
    AVG(depth_km) AS avg_depth
FROM earthquake
GROUP BY continent;
SELECT
    magType,
    ROUND(AVG(mag), 2) AS avg_magnitude,
    COUNT(*) AS total_events
FROM earthquake
GROUP BY magType
ORDER BY avg_magnitude DESC;
SELECT 
    year,
    COUNT(*) AS total_earthquakes
FROM earthquake
GROUP BY year
ORDER BY total_earthquakes DESC;
SELECT 
    month,
    COUNT(*) AS total_earthquakes
FROM earthquake
GROUP BY month
ORDER BY total_earthquakes DESC;
SELECT 
    day_of_week,
    COUNT(*) AS total_earthquakes
FROM earthquake
GROUP BY day_of_week
ORDER BY total_earthquakes DESC;
SELECT 
    HOUR(time) AS hour_of_day,
    COUNT(*) AS total_earthquakes
FROM earthquake
GROUP BY hour_of_day
ORDER BY hour_of_day;
SELECT 
    net,
    COUNT(*) AS total_events
FROM earthquake
GROUP BY net
ORDER BY total_events DESC;
SELECT
    place,
    SUM(sig) AS total_impact
FROM earthquake
WHERE sig IS NOT NULL
GROUP BY place
ORDER BY total_impact DESC
LIMIT 5;
SELECT
    alert,
    ROUND(AVG(mag * sig), 2) AS avg_estimated_loss
FROM earthquake
WHERE alert IS NOT NULL
GROUP BY alert
ORDER BY avg_estimated_loss DESC;
SELECT
    status,
    COUNT(*) AS earthquake_count
FROM earthquake
GROUP BY status;
SELECT
    type,
    COUNT(*) AS count
FROM earthquake
GROUP BY type
ORDER BY count DESC;
SELECT
    TRIM(t.type) AS data_type,
    COUNT(*) AS count
FROM earthquake e
JOIN JSON_TABLE(
    CONCAT('["', REPLACE(e.types, ',', '","'), '"]'),
    '$[*]' COLUMNS (type VARCHAR(50) PATH '$')
) AS t
GROUP BY data_type
ORDER BY count DESC;
SELECT
    id,
    place,
    mag,
    nst
FROM earthquake
WHERE nst > 50
ORDER BY nst DESC;
SELECT
    YEAR(time) AS year,
    COUNT(*) AS tsunami_events
FROM earthquake
WHERE tsunami = 1
GROUP BY YEAR(time)
ORDER BY year;
SELECT
    COALESCE(alert, 'none') AS alert_level,
    COUNT(*) AS count
FROM earthquake
GROUP BY alert_level
ORDER BY count DESC;
SELECT
    country,
    ROUND(AVG(mag), 2) AS avg_magnitude
FROM earthquake
WHERE
    mag IS NOT NULL
    AND time >= DATE_SUB(CURDATE(), INTERVAL 10 YEAR)
GROUP BY country
ORDER BY avg_magnitude DESC
LIMIT 5;
SELECT DISTINCT
    country,
    YEAR(time) AS year,
    MONTH(time) AS month
FROM earthquake
WHERE country IS NOT NULL
GROUP BY country, YEAR(time), MONTH(time)
HAVING
    SUM(depth_km < 70) > 0
    AND
    SUM(depth_km > 300) > 0;
WITH yearly_counts AS (
    SELECT
        YEAR(time) AS year,
        COUNT(*) AS total_quakes
    FROM earthquake
    GROUP BY YEAR(time)
)
SELECT
    year,
    total_quakes,
    LAG(total_quakes) OVER (ORDER BY year) AS prev_year_quakes,
    ROUND(
        (total_quakes - LAG(total_quakes) OVER (ORDER BY year)) * 100.0
        / LAG(total_quakes) OVER (ORDER BY year),
        2
    ) AS yoy_growth_percent
FROM yearly_counts;
SELECT
    country AS region,
    COUNT(*) AS quake_count,
    ROUND(AVG(mag), 2) AS avg_magnitude,
    ROUND(COUNT(*) * AVG(mag), 2) AS activity_score
FROM earthquake
WHERE mag IS NOT NULL
GROUP BY country
ORDER BY activity_score DESC
LIMIT 3;
SELECT
    country,
    ROUND(AVG(depth_km), 2) AS avg_depth
FROM earthquake
WHERE latitude BETWEEN -5 AND 5
  AND country IS NOT NULL
GROUP BY country;
SELECT
    country,
    SUM(depth_km < 70) AS shallow_quakes,
    SUM(depth_km > 300) AS deep_quakes,
    ROUND(
        SUM(depth_km < 70) / NULLIF(SUM(depth_km > 300), 0),
        2
    ) AS shallow_to_deep_ratio
FROM earthquake
WHERE country IS NOT NULL
GROUP BY country
ORDER BY shallow_to_deep_ratio DESC;
SELECT
    ROUND(
        AVG(CASE WHEN tsunami = 1 THEN mag END) -
        AVG(CASE WHEN tsunami = 0 THEN mag END),
        2
    ) AS avg_magnitude_difference
FROM earthquake
WHERE mag IS NOT NULL;
SELECT
    id,
    place,
    rms,
    gap,
    ROUND((rms + gap) / 2, 2) AS error_score
FROM earthquake
WHERE rms IS NOT NULL AND gap IS NOT NULL
ORDER BY error_score DESC
LIMIT 10;
WITH ordered_quakes AS (
    SELECT
        id,
        time,
        latitude,
        longitude,
        LAG(time) OVER (ORDER BY time) AS prev_time,
        LAG(latitude) OVER (ORDER BY time) AS prev_lat,
        LAG(longitude) OVER (ORDER BY time) AS prev_lon
    FROM earthquake
)
SELECT
    id,
    time,
    prev_time,
    ROUND(
        6371 * ACOS(
            COS(RADIANS(latitude)) * COS(RADIANS(prev_lat)) *
            COS(RADIANS(longitude) - RADIANS(prev_lon)) +
            SIN(RADIANS(latitude)) * SIN(RADIANS(prev_lat))
        ),
        2
    ) AS distance_km
FROM ordered_quakes
WHERE
    TIMESTAMPDIFF(MINUTE, prev_time, time) <= 60
HAVING distance_km <= 50;
SELECT
    country,
    COUNT(*) AS deep_focus_count
FROM earthquake
WHERE depth_km > 300
  AND country IS NOT NULL
GROUP BY country
ORDER BY deep_focus_count DESC;

