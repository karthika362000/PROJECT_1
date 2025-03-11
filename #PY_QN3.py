#PY_QN3
#Question3- doubles competitor ranking data:
#featching the data from double competition ranking table(through api copied link):
import requests

url = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json?api_key=thR9aCu2MyItRQxoxTnfnAWvSiInIm1jjDfF7Vhn"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)


json_data = response.text
json_data


import pandas as pd
import json
import mysql.connector

#JSON STR to a Python dict:
data = json.loads(json_data)

#Extract rankings(table->1)
df_rankings = pd.json_normalize(data["rankings"], 
                                record_path=["competitor_rankings"], 
                                meta=["year", "week"], 
                                record_prefix="rank_")

#Extract competitors(table->2)
df_competitors = df_rankings[["rank_competitor.id", "rank_competitor.name", 
                              "rank_competitor.country", "rank_competitor.country_code", 
                              "rank_competitor.abbreviation"]].drop_duplicates()

#Changes column names to match SQL table column names:
df_rankings = df_rankings.rename(columns={
    "rank_rank": "rank",
    "rank_movement": "movement",
    "rank_points": "points",
    "rank_competitions_played": "competitions_played",
    "rank_competitor.id": "competitor_id"
})

df_rankings = df_rankings[["rank", "movement", "points", "competitions_played", "competitor_id"]]

#Matches df_competitors columns with SQL table names:
df_competitors = df_competitors.rename(columns={
    "rank_competitor.id": "competitor_id",
    "rank_competitor.name": "name",
    "rank_competitor.country": "country",
    "rank_competitor.country_code": "country_code",
    "rank_competitor.abbreviation": "abbreviation"
})


df_competitors
df_rankings


null_count = df_competitors['country_code'].isnull().sum()
null_count


check_KVS_present = (df_competitors['country_code'] == 'KVS').sum()
check_KVS_present


df_competitors = df_competitors.copy()
df_competitors['country_code'] = df_competitors['country_code'].fillna('KVS')


df_competitors[df_competitors['country_code'] == 'KVS']


import mysql.connector
import pandas as pd
import numpy as np

# Connect to MySQL Database
# Establish connection to MySQL 
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sk@112308",
    database="Tennis_project"
)

cursor = conn.cursor()

#Creating Competitors table (if it doesn’t exist).competitor_id is the Primary Key (unique ID for each competitor).
# Create Tables (Fixed "rank" Issue)
create_competitors_table = """
CREATE TABLE IF NOT EXISTS Competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    abbreviation VARCHAR(10) NOT NULL
);
"""

#Creating Rankings table (if it doesn’t exist) & Stores ranking details:
#rank_id is the Primary Key (unique for each ranking record).
#Fixed issue: Changed column name from "rank" to "player_rank" (because rank is a reserved word in SQL)
create_rankings_table = """
CREATE TABLE IF NOT EXISTS Rankings (
    rank_id INT PRIMARY KEY AUTO_INCREMENT,
    player_rank INT NOT NULL,  -- FIXED: Changed from 'rank' to 'player_rank'
    movement INT NOT NULL,
    points INT NOT NULL,
    competitions_played INT NOT NULL,
    competitor_id VARCHAR(50),
    FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
);
"""

#Deleting the Rankings and Competitors tables if they already exist.This clears old data before creating new tables:
cursor.execute("DROP TABLE IF EXISTS Rankings;")
cursor.execute("DROP TABLE IF EXISTS Competitors;")

print("Tables dropped before creating")

cursor.execute(create_competitors_table)
cursor.execute(create_rankings_table)
conn.commit()

print("Tables created successfully!")

#Replaces NaN (missing values) with None:
df_competitors = df_competitors.replace({np.nan: None})
df_rankings = df_rankings.replace({np.nan: None})

#Inserting competitors into the Competitors table.ON DUPLICATE KEY UPDATE → If the competitor_id already exists, it updates the competitor’s details instead of inserting again.
competitor_insert_query = """
INSERT INTO Competitors (competitor_id, name, country, country_code, abbreviation) 
VALUES (%s, %s, %s, %s, %s) 
ON DUPLICATE KEY UPDATE 
    name = VALUES(name),
    country = VALUES(country),
    country_code = VALUES(country_code),
    abbreviation = VALUES(abbreviation);
"""

#Converting df_competitors from a Pandas DataFrame to a list of tuples:
competitor_data = df_competitors.to_records(index=False).tolist()
cursor.executemany(competitor_insert_query, competitor_data)
conn.commit()
print("Competitors inserted successfully!")

#Inserting Data into Rankings Table:
ranking_insert_query = """
INSERT INTO Rankings (player_rank, movement, points, competitions_played, competitor_id) 
VALUES (%s, %s, %s, %s, %s);
"""

ranking_data = df_rankings.to_records(index=False).tolist()  # Convert DataFrame to list of tuples
cursor.executemany(ranking_insert_query, ranking_data)
conn.commit()
print("Rankings inserted successfully!")

# Close Connection
cursor.close()
conn.close()
print("Database connection closed.")