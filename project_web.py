import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# Connecting to MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sk@112308",
        database="Tennis_project"
    )

# Fetching data
def run_query(query, params=None):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return pd.DataFrame(data, columns=columns)

# Streamlit UI Setup
st.set_page_config(page_title="Tennis Analytics Dashboard", layout="wide")
st.title("🎾 Tennis Data Analysis Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
year = st.sidebar.number_input("Year", min_value=2000, max_value=2030, value=2024)
week = st.sidebar.number_input("Week", min_value=1, max_value=52, value=48)
gender = st.sidebar.selectbox("Gender", ["men", "women"])
rank_range = st.sidebar.slider("Rank Range", 1, 100, (1, 50))
search_competitor = st.sidebar.text_input("Search Competitor", "")

# SQL Queries
queries = {
    "Competitions by Category": """
        SELECT c.competition_name, cat.category_name 
        FROM Competitions c 
        JOIN Categories cat ON c.category_id = cat.category_id;
    """,
    "Count Competitions per Category": """
        SELECT cat.category_name, COUNT(c.competition_id) AS total_competitions 
        FROM Competitions c 
        JOIN Categories cat ON c.category_id = cat.category_id 
        GROUP BY cat.category_name;
    """,
    "Top Competitors": """
        SELECT r.player_rank, c.name, r.points 
        FROM Rankings r 
        JOIN Competitors c ON r.competitor_id = c.competitor_id 
        WHERE r.player_rank BETWEEN %s AND %s 
        ORDER BY r.player_rank ASC;
    """,
    "Venues by Complex": """
        SELECT v.venue_name, cx.complex_name, v.country, v.timezone 
        FROM Venues v 
        JOIN Complexes cx ON v.complex_id = cx.complex_id;
    """
}

# Dropdown to select query
selected_query = st.selectbox("Select Query", list(queries.keys()))

# Run query when button is clicked
if st.button("Run Query"):
    query = queries[selected_query]
    params = (rank_range[0], rank_range[1]) if "Top Competitors" in selected_query else None
    result = run_query(query, params)
    
    if result.empty:
        st.warning("No data found!")
    else:
        st.write(f"**Executed Query:** `{query}`")
        st.dataframe(result, height=400)

        # Visualization
        if "Count Competitions per Category" in selected_query:
            fig = px.bar(result, x="category_name", y="total_competitions", title="Competitions per Category")
            st.plotly_chart(fig)
        elif "Top Competitors" in selected_query:
            fig = px.line(result, x="player_rank", y="points", title="Ranking Points Trend")
            st.plotly_chart(fig)
        elif "Venues by Complex" in selected_query:
            fig = px.pie(result, names="country", title="Venues Distribution by Country")
            st.plotly_chart(fig)

# Summary Statistics
st.sidebar.subheader("Summary Statistics")
total_competitions = run_query("SELECT COUNT(*) FROM Competitions;").iloc[0, 0]
total_competitors = run_query("SELECT COUNT(*) FROM Competitors;").iloc[0, 0]
highest_ranking = run_query("SELECT name, player_rank, points FROM Rankings JOIN Competitors USING(competitor_id) ORDER BY player_rank ASC LIMIT 1;")

st.sidebar.write(f"**Total Competitions:** {total_competitions}")
st.sidebar.write(f"**Total Competitors:** {total_competitors}")
if not highest_ranking.empty:
    st.sidebar.write(f"**Top Competitor:** {highest_ranking.iloc[0, 0]} (Rank: {highest_ranking.iloc[0, 1]}, Points: {highest_ranking.iloc[0, 2]})")
