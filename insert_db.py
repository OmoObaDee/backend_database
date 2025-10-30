from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pymysql.constants import CLIENT
import os
load_dotenv()

# Build DB URL from environment variables
db_url = f'mysql+pymysql://{os.getenv("dbuser")}:{os.getenv("dbpassword")}@{os.getenv("dbhost")}:{os.getenv("dbport")}/{os.getenv("dbname")}'
# Create engine with support for multiple statements
engine = create_engine(db_url, connect_args={"client_flag": CLIENT.MULTI_STATEMENTS})
# Create session
Session = sessionmaker(bind=engine)
db = Session()
# Define all create table queries

# Insert query
query = text("""
INSERT INTO courses (
    id, title,level
) VALUES (
    5, 'ict', 'beginner',
    6, 'maths', 'intermediate'  ,
    7, 'english', 'advanced',
    8, 'loan_data', 'advanced',
    9, 'data_science', 'advanced',
    10, 'web_development', 'beginner'

""")

# db.execute(query)
# db.commit()

print("✅ Data inserted successfully!")

