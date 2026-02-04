import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.title("🌍 Global Seismic Trends Dashboard")
st.write("Earthquake analysis using USGS data")

engine = create_engine(
    "mysql+mysqlconnector://root:Devi%4025@localhost:3306/earthquake_db"
)

df = pd.read_sql("SELECT * FROM earthquake", engine)

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.sidebar.header("📌 Select Task")

task = st.sidebar.selectbox(
    "Choose a Task",
    [f"Task {i}" for i in range(1, 29)]
)

if task == "Task 1":
    st.subheader("1️⃣ Top 10 Strongest Earthquakes (Magnitude)")

    task1 = df.sort_values("mag", ascending=False).head(10)

    st.dataframe(task1[["place", "mag", "depth_km", "time"]])

if task == "Task 2":
    st.subheader("2️⃣ Top 10 Deepest Earthquakes")

    task2 = df.sort_values("depth_km", ascending=False).head(10)

    st.dataframe(task2[["place", "depth_km", "mag", "time"]])

if task == "Task 3":
    st.subheader("3️⃣ Shallow (<50 km) and Strong (>7.5) Earthquakes")

    task3 = df[(df["depth_km"] < 50) & (df["mag"] > 7.5)]

    st.write("Total Events:", task3.shape[0])
    st.dataframe(task3[["place", "mag", "depth_km", "time"]])

if task == "Task 4":
    st.subheader("4️⃣ Average Earthquake Depth per Continent")

    query = """
    SELECT
        CASE
            WHEN country IN ('japan', 'china', 'india', 'indonesia') THEN 'Asia'
            WHEN country IN ('chile', 'peru', 'mexico') THEN 'South America'
            WHEN country IN ('united states', 'canada') THEN 'North America'
            WHEN country IN ('italy', 'greece', 'turkey') THEN 'Europe'
            WHEN country IN ('new zealand') THEN 'Oceania'
            ELSE 'Other'
        END AS continent,
        AVG(depth_km) AS avg_depth
    FROM earthquake
    GROUP BY continent
    """

    task4 = pd.read_sql(query, engine)

    st.dataframe(task4)

if task == "Task 5":
    st.subheader("5️⃣ Average Magnitude per Magnitude Type")

    task5 = df.groupby("magType")["mag"].mean().reset_index()
    task5.columns = ["Magnitude Type", "Average Magnitude"]

    st.dataframe(task5)

if task == "Task 6":
    st.subheader("6️⃣ Year with Most Earthquakes")

    task6 = df["year"].value_counts().reset_index()
    task6.columns = ["Year", "Count"]

    st.dataframe(task6.head(1))

if task == "Task 7":
    st.subheader("7️⃣ Month with Highest Number of Earthquakes")

    query = """
    SELECT 
        month,
        COUNT(*) AS total_earthquakes
    FROM earthquake
    GROUP BY month
    ORDER BY total_earthquakes DESC
    """

    task7 = pd.read_sql(query, engine)

    st.dataframe(task7)

    top_month = task7.iloc[0]

    st.success(
        f"📊 Highest earthquakes occurred in **{top_month['month']}** "
        f"with **{top_month['total_earthquakes']}** events"
    )

if task == "Task 8":
    st.subheader("8️⃣ Day of Week with Most Earthquakes")

    query = """
    SELECT 
        day_of_week,
        COUNT(*) AS total_earthquakes
    FROM earthquake
    GROUP BY day_of_week
    ORDER BY total_earthquakes DESC
    """

    task8 = pd.read_sql(query, engine)

    st.dataframe(task8)

    top_day = task8.iloc[0]

    st.success(
        f"📅 Most earthquakes occurred on **{top_day['day_of_week']}** "
        f"with **{top_day['total_earthquakes']}** events"
    )

if task == "Task 9":
    st.subheader("9️⃣ Earthquakes per Hour of Day")

    query = """
    SELECT 
        HOUR(time) AS hour_of_day,
        COUNT(*) AS total_earthquakes
    FROM earthquake
    GROUP BY hour_of_day
    ORDER BY hour_of_day
    """

    task9 = pd.read_sql(query, engine)

    st.dataframe(task9)

    st.bar_chart(
        task9.set_index("hour_of_day")["total_earthquakes"]
    )

if task == "Task 10":
    st.subheader("🔟 Most Active Reporting Network")

    task10 = df["net"].value_counts().reset_index()
    task10.columns = ["Network", "Count"]

    st.dataframe(task10.head(1))

if task == "Task 11":
    st.subheader("1️⃣1️⃣ Top 5 Places with Highest Casualties / Impact")

    query = """
    SELECT
        place,
        SUM(sig) AS total_impact
    FROM earthquake
    WHERE sig IS NOT NULL
    GROUP BY place
    ORDER BY total_impact DESC
    LIMIT 5
    """

    task11 = pd.read_sql(query, engine)

    st.dataframe(task11)

    st.bar_chart(
        task11.set_index("place")["total_impact"]
    )

if task == "Task 12":
    st.subheader("1️⃣2️⃣ Average Economic Loss by Alert Level")

    query = """
    SELECT
        alert,
        ROUND(AVG(mag * sig), 2) AS avg_estimated_loss
    FROM earthquake
    WHERE alert IS NOT NULL
    GROUP BY alert
    ORDER BY avg_estimated_loss DESC;
    """

    task12 = pd.read_sql(query, engine)

    st.dataframe(task12)

    st.bar_chart(
        task12.set_index("alert")["avg_estimated_loss"]
    )
if task == "Task 13":
    st.subheader("1️⃣3️⃣ Count of Reviewed vs Automatic Earthquakes")

    query = """
    SELECT
        status,
        COUNT(*) AS earthquake_count
    FROM earthquake
    GROUP BY status;
    """

    task13 = pd.read_sql(query, engine)

    st.dataframe(task13)

    st.bar_chart(
        task13.set_index("status")["earthquake_count"]
    )
if task == "Task 14":
    st.subheader("1️⃣4️⃣ Count by Earthquake Type")

    query = """
    SELECT
        type,
        COUNT(*) AS count
    FROM earthquake
    GROUP BY type
    ORDER BY count DESC;
    """

    task14 = pd.read_sql(query, engine)

    st.dataframe(task14)

    st.bar_chart(
        task14.set_index("type")["count"]
    )
if task == "Task 15":
    st.subheader("1️⃣5️⃣ Number of Earthquakes by Data Type")

    query = """
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
    """

    task15 = pd.read_sql(query, engine)

    st.dataframe(task15)

    st.bar_chart(
        task15.set_index("data_type")["count"]
    )

if task == "Task 16":
    st.subheader("1️⃣6️⃣ Events with High Station Coverage (nst > 50)")

    query = """
    SELECT
        id,
        place,
        mag,
        nst
    FROM earthquake
    WHERE nst > 50
    ORDER BY nst DESC;
    """

    task16 = pd.read_sql(query, engine)

    st.dataframe(task16)

    st.write("Total High-Coverage Events:", task16.shape[0])

if task == "Task 17":
    st.subheader("1️⃣7️⃣ Number of Tsunamis Triggered per Year")

    query = """
    SELECT
        YEAR(time) AS year,
        COUNT(*) AS tsunami_events
    FROM earthquake
    WHERE tsunami = 1
    GROUP BY YEAR(time)
    ORDER BY year;
    """

    task17 = pd.read_sql(query, engine)

    st.dataframe(task17)

    st.line_chart(
        task17.set_index("year")["tsunami_events"]
    )
if task == "Task 18":
    st.subheader("1️⃣8️⃣ Count of Earthquakes by Alert Level")

    query = """
    SELECT
        COALESCE(alert, 'none') AS alert_level,
        COUNT(*) AS count
    FROM earthquake
    GROUP BY alert_level
    ORDER BY count DESC;
    """

    task18 = pd.read_sql(query, engine)

    st.dataframe(task18)

    st.bar_chart(
        task18.set_index("alert_level")["count"]
    )
if task == "Task 19":
    st.subheader("1️⃣9️⃣ Top 5 Countries with Highest Average Earthquake Magnitude (Past 10 Years)")

    query = """
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
    """

    task19 = pd.read_sql(query, engine)

    st.dataframe(task19)

    st.bar_chart(
        task19.set_index("country")["avg_magnitude"]
    )
if task == "Task 20":
    st.subheader("2️⃣0️⃣ Countries with Both Shallow and Deep Earthquakes in the Same Month")

    query = """
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
    """

    task20 = pd.read_sql(query, engine)

    st.dataframe(task20)

    st.write("Total such occurrences:", task20.shape[0])

if task == "Task 21":
    st.subheader("2️⃣1️⃣ Year-over-Year Growth Rate of Earthquakes (Global)")

    query = """
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
    """

    task21 = pd.read_sql(query, engine)

    st.dataframe(task21)

    st.line_chart(
        task21.set_index("year")["total_quakes"]
    )
if task == "Task 22":
    st.subheader("2️⃣2️⃣ Top 3 Most Seismically Active Regions")

    query = """
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
    """

    task22 = pd.read_sql(query, engine)

    st.dataframe(task22)

    st.bar_chart(
        task22.set_index("region")["activity_score"]
    )
if task == "Task 23":
    st.subheader("2️⃣3️⃣ Average Earthquake Depth Near the Equator (±5° Latitude)")

    query = """
    SELECT
        country,
        ROUND(AVG(depth_km), 2) AS avg_depth
    FROM earthquake
    WHERE latitude BETWEEN -5 AND 5
      AND country IS NOT NULL
    GROUP BY country;
    """

    task23 = pd.read_sql(query, engine)

    st.dataframe(task23)

    st.bar_chart(
        task23.set_index("country")["avg_depth"]
    )
if task == "Task 24":
    st.subheader("2️⃣4️⃣ Countries with Highest Shallow-to-Deep Earthquake Ratio")

    query = """
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
    """

    task24 = pd.read_sql(query, engine)

    st.dataframe(task24)

    st.bar_chart(
        task24.set_index("country")["shallow_to_deep_ratio"]
    )
if task == "Task 25":
    st.subheader("2️⃣5️⃣ Average Magnitude Difference (Tsunami vs Non-Tsunami)")

    query = """
    SELECT
        ROUND(
            AVG(CASE WHEN tsunami = 1 THEN mag END) -
            AVG(CASE WHEN tsunami = 0 THEN mag END),
            2
        ) AS avg_magnitude_difference
    FROM earthquake
    WHERE mag IS NOT NULL;
    """

    task25 = pd.read_sql(query, engine)

    diff_value = task25.iloc[0]["avg_magnitude_difference"]

    st.metric(
        label="Avg Magnitude Difference",
        value=diff_value
    )
if task == "Task 26":
    st.subheader("2️⃣6️⃣ Events with Lowest Data Reliability (Highest Error Score)")

    query = """
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
    """

    task26 = pd.read_sql(query, engine)

    st.dataframe(task26)

    st.bar_chart(
        task26.set_index("id")["error_score"]
    )
if task == "Task 27":
    st.subheader("2️⃣7️⃣ Consecutive Earthquakes Within 50 km and 1 Hour")

    query = """
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
    """

    task27 = pd.read_sql(query, engine)

    st.dataframe(task27)

    st.write("Total close consecutive pairs:", task27.shape[0])
if task == "Task 28":
    st.subheader("2️⃣8️⃣ Regions with Highest Frequency of Deep-Focus Earthquakes")

    query = """
    SELECT
        country,
        COUNT(*) AS deep_focus_count
    FROM earthquake
    WHERE depth_km > 300
      AND country IS NOT NULL
    GROUP BY country
    ORDER BY deep_focus_count DESC;
    """

    task28 = pd.read_sql(query, engine)

    st.dataframe(task28)

    st.bar_chart(
        task28.set_index("country")["deep_focus_count"]
    )
