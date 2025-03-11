#PY_QN1
#Question1-competition data
#featching the data from competition table(through api copied link):
import requests


url = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json?api_key=thR9aCu2MyItRQxoxTnfnAWvSiInIm1jjDfF7Vhn" #getting data from api sportradar link:

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)


import json #converting json file
data = json.loads(response.text)


data #printing the data from previous input


categories = [
    {"category_id": i["category"]["id"], "category_name": i["category"]["name"]}
    for i in data.get("competitions", [])
    if "category" in i and "id" in i["category"] and "name" in i["category"]
]


print(categories) #here am creating the categories as per the question 1:


print(len(data['competitions'])) #printing the length of the first question ( two tables ):
print(len(categories))


unique_categories = {c["category"]["id"]: c["category"]["name"] for c in data.get("competitions", []) if "category" in c}
print(unique_categories)


competitions = [] #(table)
for i in data.get('competitions', []):  
    competition_id = i.get('id')
    name = i.get('name')
    parent_id = i.get('parent_id')  #only thing which will be missing 
    comp_type = i.get('type')
    gender = i.get('gender')

    category = i.get('category', {})  #category dict
    category_id = category.get('id')  #Get category ID

    if competition_id and name and category_id:  #dobule check the exist field required:
        competitions.append([
            competition_id, 
            name, 
            parent_id, 
            comp_type, 
            gender, 
            category_id
        ])
competitions


print(len(data['competitions'])) #here i am printing the whole length of the competitions
print(len(categories))
print(len(categories))


import mysql.connector
#Connecting MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sk@112308"
)


cursor = conn.cursor() #execute SQL commands through this:


#Step1-> Creating Database (if it's not exists):
cursor.execute("CREATE DATABASE IF NOT EXISTS Tennis_project")

#Selecting the database here:
cursor.execute("USE Tennis_project")


#Step2->Creating Categories Table:
create_categories_table = """
CREATE TABLE IF NOT EXISTS Categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);
"""


#Step->3->Creating Competitions Table:
create_competitions_table = """
CREATE TABLE IF NOT EXISTS Competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    parent_id VARCHAR(50) NULL,
    type VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    category_id VARCHAR(50),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE CASCADE
);
"""


#Queries_execution:
cursor.execute(create_categories_table)
cursor.execute(create_competitions_table)


#Commit and close connection from the above datas:
conn.commit()
cursor.close()
conn.close()


print("Database and tables created successfully!")

#Step4->Inserting the data into categories and competitions:
conn = mysql.connector.connect(
    host="localhost",
    user="root", 
    password="Sk@112308",
    database="Tennis_project"
    )


cursor = conn.cursor()


#Deleting data from Categories and Competitions tables(optional):
'''cursor.execute("truncate table Categories;")
cursor.execute("truncate table Competitions;")'''


#Insert Categories into Database (Avoids_Duplicates):
for category_id, category_name in unique_categories.items():
    cursor.execute(
        "INSERT IGNORE INTO Categories (category_id, category_name) VALUES (%s, %s)",
        (category_id, category_name)
    )


for each_competition in competitions:
    cursor.execute('INSERT INTO Competitions (competition_id, competition_name, parent_id, type, gender, category_id) VALUES (%s, %s, %s, %s, %s, %s)', each_competition)


#Commiting and close connection:
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully into Categories & Competitions tables!")

#Featched data from api
#Connects to MySQL
#Cleared tables
#Insertred categories (avoiding duplicates)
#Insertred competitions
#Saved and closed the database
#Printed output(success or failure)


