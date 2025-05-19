import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Get credentials
host = os.getenv("SQL_HOST")
user = os.getenv("SQL_USER")
password = os.getenv("SQL_PASSWORD")
database = os.getenv("SQL_DATABASE")

# Connect to MySQL
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS sys_command (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    path VARCHAR(1000)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS web_command (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    url VARCHAR(1000)
)
""")

conn.commit()
