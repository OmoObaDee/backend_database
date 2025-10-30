from database_pc import db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import uvicorn
import bcrypt
from middleware import create_token
from middleware import verify_token
from fastapi import Depends
load_dotenv()
app = FastAPI(title="Simple API", version="1.0.0")
token_time = int(os.getenv("token_time"))
class Simple(BaseModel):
    name: str = Field(..., example="Sam Larry")
    email: str = Field(..., example="sam@email.com")
    password: str = Field(..., example="sam123")
    usertype : str = Field(...,example="student")
class valid(BaseModel):
    course_title: str = Field(...,example="Backend Devloper")
    level: str = Field(...,example="300 level")
@app.post("/signup")
def signup(input: Simple):
    try:
        duplicate_query = text(
            """
            SELECT * FROM user
            WHERE email = :email
            """
        )
        existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
        if existing:
            print("Email already exists")
            # raise HTTPException(status_code=400, detail="Email already exists")
        query = text("""
            INSERT INTO user (name, email, password, usertype)
            VALUES (:name, :email, :password, :usertype)
                     """)
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(input.password.encode("utf-8"),salt)
        db.execute(query, {"name":input.name, "email":input.email, "password": hashedPassword, "usertype": input.usertype})
        db.commit()
        return {"message": "User created sucessfully",
                "data": {"name":input.name, "email":input.email, "usertype":input.usertype}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
class loginrequest(BaseModel):
    email: str =Field(..., example="sam@email.com")
    password: str = Field(..., example="sam123")
@app.post("/login")
def login(input:loginrequest):
    try:
        query = text("""
        SELECT * FROM user WHERE email = :email
""")
        result = db.execute(query, {"email": input.email}).fetchone()
        if not result:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        verified_password = bcrypt.checkpw(input.password.encode("utf-8"), result.password.encode("utf-8"))
        if not verified_password:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        encoded_token = create_token(details={"id":result.id,"email":result.email,"usertype":result.usertype},expiry=token_time)
        return {
            "message":"Login Sucessful",
            "token": encoded_token
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
class valid(BaseModel):
    title: str = Field(...,example="Backend Devloper")
    level: str = Field(...,example="300 level")
@app.post("/courses")
def addcourse(input:valid, user_data= Depends(verify_token)):
    try:
        print(user_data)
        if user_data["usertype"] != "admin":
            raise HTTPException(status_code=401, detail="You arent authorized to add a course")
        query=text("""
            INSERT INTO course(title,level)
                VALUES(:title,:level)
""")
        db.execute(query, {"title":input.title, "level":input.level})
        db.commit()
        return {
        "message": "Course created sucessfully",
        "data": {
            "title":input.title,
            "level":input.level
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
class id(BaseModel):
    courseid: int = Field(..., example= 1)
@app.post("/enroll")
def enrollcourse(input:id, user_data = Depends(verify_token)):
    try:
        print(user_data)
        if user_data["usertype"] != "student":
            raise HTTPException(status_code=401, detail="You are not authorized to enroll for a course")
        query=text("""
            INSERT INTO Enrollment(userid,courseid)
                VALUES(:userid,:courseid)
                   """)
        db.execute(query, {"userid":user_data["id"], "courseid":input.courseid})
        db.commit()
        return {
        "message": "Course created sucessfully",
        "data": {
            "userid":user_data["id"],
            "courseid":input.courseid
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))