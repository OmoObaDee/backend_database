# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.exc import SQLAlchemyError
# from dotenv import load_dotenv
# import os   

# load_dotenv()
# #db url= dialect+driver://duser;dbpassword;dbhost;dbport;dbname
# db_url=f"mysql+pymysql://{os.getenv("dbuser")}:{os.getenv("dbpassword")}@{os.getenv("dbhost")}:{os.getenv("dbport")}/{os.getenv("dbname")}"
# engine = create_engine(db_url)
# session = sessionmaker(bind=engine)
# db = session()
# query = text("SELECT * FROM user")
# users = db.execute(query).fetchall()
# print(users)


# create_tables_query = text("""
#                            CREATE TABLE IF NOT EXISTS user (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     username VARCHAR(50) NOT NULL UNIQUE,
#     email VARCHAR(100) NOT NULL UNIQUE,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# """);


# CREATE TABLE IF NOT EXISTS courses (
#     course_id INT PRIMARY KEY AUTO_INCREMENT,
#     course_name VARCHAR(100) NOT NULL,
#     title VARCHAR(100) NOT NULL,
#     LELVEL VARCHAR(50) NOT NULL,
#     description TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# CREATE TABLE IF NOT EXISTS enrollments (
#     enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
#     user_id INT NOT NULL,
#     course_id INT NOT NULL,
#     level VARCHAR(50),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES user(id),
#     FOREIGN KEY (course_id) REFERENCES courses(course_id)
# );

# try:
#     db.execute(create_tables_query)
#     db.commit()
#     print("Tables created successfully.")
# except SQLAlchemyError as e:
#     print(f"Error creating tables: {e}")
#     db.rollback()

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from pymysql.constants import CLIENT
load_dotenv()
db_url = f'mysql+pymysql://{os.getenv("dbuser")}:{os.getenv("dbpassword")}@{os.getenv("dbhost")}:{os.getenv("dbport")}/{os.getenv("dbname")}'
engine = create_engine(
    db_url,
    connect_args={"client_flag": CLIENT.MULTI_STATEMENTS}
)
Session = sessionmaker(bind=engine)
with Session() as db:
    create_table_user = text("""
    CREATE TABLE IF NOT EXISTS `user` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE
    );
    """)
    create_table_courses = text("""
    CREATE TABLE IF NOT EXISTS courses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        level VARCHAR(100) NOT NULL,
        description TEXT NOT NULL
    );
    """)
    create_table_enrollments = text("""
    CREATE TABLE IF NOT EXISTS enrollments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        course_id INT,
        FOREIGN KEY (user_id) REFERENCES `user`(id),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    );
    """)
    for ddl in (create_table_user, create_table_courses, create_table_enrollments):
        db.execute(ddl)
    db.commit()
