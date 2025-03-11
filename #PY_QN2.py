#PY_QN2
#question 2 (complexes_data )
#featching the data from complex table(through api copied link):
import requests

url = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json?api_key=thR9aCu2MyItRQxoxTnfnAWvSiInIm1jjDfF7Vhn" #getting data from api sportradar link:

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)


import json #like i did for the ques1:
data = json.loads(response.text)
data


import json #importing json lib:
import pandas as pd #importing pandas to work with table data:
df_complexes = pd.json_normalize(data["complexes"],sep="_") #slowly seperating the complaexes data from json file:
df_complexes #shows the table output:


df_complexes = df_complexes.rename(columns={"id": "complex_id", "name": "complex_name"}) #Changing column id to complex_id & Changing column name to complex_name:
df_complexes #this will update the changesa nd print the final updated output:


#Extracting venue details from each complex as data,Checking if "venues" exist in the complex before extracting details,Creating list of dict's, where each dict represents a venue.
#Storing the data in a Pandas DF->(df_venues),Printing df_venues, showing venues in a proper table.
venues_data = [
    {
        "venue_id": v["id"],
        "venue_name": v["name"],
        "city_name": v["city_name"],
        "country_name": v["country_name"],
        "country_code": v["country_code"],
        "timezone": v["timezone"],
        "complex_id": c["id"]  # Foreign Key reference
    }
    for c in data["complexes"] if "venues" in c
    for v in c["venues"]
]
df_venues = pd.DataFrame(venues_data)

df_venues


#eliminating duplicate rows in df_complexes based on the ("complex_id") column:
df_complexes = df_complexes.drop_duplicates(subset=["complex_id"])
#eliminating duplicate rows in (df_venues) based on the ("venue_id") column:
df_venues = df_venues.drop_duplicates(subset=["venue_id"])
#making sure complex and venue appears once in their respective DF & Stored flitered DF into df_complexes and df_venues:


df_complexes #filtered output of complex table:
df_venues #filtered output of venues table:


#connecting MySQL:
#Creating complexes and venues table here:
import mysql.connector

# Establish connection to MySQL 
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sk@112308",
    database="Tennis_project"
)

cursor = conn.cursor() #execute SQL commands through this

create_complexes_table = """
CREATE TABLE IF NOT EXISTS Complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(100) NOT NULL
);
"""
cursor.execute(create_complexes_table)

# Create Venues table with foreign key constraint
create_venues_table = """
CREATE TABLE IF NOT EXISTS Venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    timezone VARCHAR(100) NOT NULL,
    complex_id VARCHAR(50),
    FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id) ON DELETE CASCADE
);
"""
#Foreign Key is (complex_id) between Venues and Complexes
cursor.execute(create_venues_table)


#inserting new complex (complex_id, complex_name).if complex_id already exists, it updates complex_name instead of duplicate:
complexes_insert_query = """
INSERT INTO Complexes (complex_id, complex_name) 
VALUES (%s, %s) 
ON DUPLICATE KEY UPDATE complex_name = VALUES(complex_name);
"""

#Converting Pandas DF (df_complexes) to a list of tuples,using (executemany()) to insert multiple rows at once.Commit the changes to save them in the db:
complexes_data = list(df_complexes.itertuples(index=False, name=None))  

cursor.executemany(complexes_insert_query, complexes_data)
conn.commit()

#Inserting venue's details (venue_id, venue_name, city_name, etc.).venue_id already exists, updates the venue’s details instead of inserting a duplicate:
venues_insert_query = """
INSERT INTO Venues (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id) 
VALUES (%s, %s, %s, %s, %s, %s, %s) 
ON DUPLICATE KEY UPDATE 
    venue_name = VALUES(venue_name),
    city_name = VALUES(city_name),
    country_name = VALUES(country_name),
    country_code = VALUES(country_code),
    timezone = VALUES(timezone),
    complex_id = VALUES(complex_id);
"""

#Converting df_venues DF to a list of tuples for MySQL insertion:
venues_data = list(df_venues.itertuples(index=False, name=None))  

#Commiting changes to save them in the MySQL:
cursor.executemany(venues_insert_query, venues_data)
conn.commit()


cursor.execute("select * from complexes") #This gets all data from Complexes table in MySQL and prints each row:
for i in cursor: #using loop to to return each query:
    print(i)


conn.commit()
cursor.close()
conn.close()