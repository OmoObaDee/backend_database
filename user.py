from database import db
from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import uvicorn
import bcrypt
from middleware import create_token, verify_token
load_dotenv()


app=FastAPI(title="Simple App", version="1.0.0")
token_time = int(os.getenv("token_time"))
class simple(BaseModel):
    name: str = Field(..., example= "Oludayo Oluwole")
    email: str= Field(..., example= "prince01ben@gmail.com")
    password: str=Field(..., example= "Faithfully.1")
    userType: str = Field(..., example="student")

    
@app.get("/", description="This endpoint just return a welcome message")
def root():
    return {"Message": "Welcome to my FastAPI App"}


@app.post("/signup")
def signUp(input:simple):
    try:
        duplicate_query=text("""
            SELECT * FROM users
            WHERE email=:email
                            """)
        existing = db.execute(duplicate_query,{"email": input.email})
        if existing:
            print("Email already exist")
        query= text("""
            INSERT INTO users (name, email, password, userType)
            VALUES(:name, :email, :password, :userType)
        """)
        # hashing password
        salt = bcrypt.gensalt()
        hashedpassword = bcrypt.hashpw(input.password.encode('utf-8'), salt)
        #print(hashedpassword)
        # mapping data
        db.execute(query, {"name": input.name, "email": input.email, "password": hashedpassword, "userType": input.userType})
        #data= {"name":input.name, "email":input.email, "password":hashedpassword}
        #db.execute(query,data)
        db.commit()
        return {"Message": "User created sucessfuly",
                "data": {"name": input.name, "email": input.email, "userType": input.userType}}
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))
    

class LoginRequest(BaseModel):
    email: str = Field(..., example="omoobadee1@gmail.com")
    password: str = Field(..., example= "Faithfully.1")

@app.post("/login")
def login(input: LoginRequest):
    try:
        query = text("""
         SELECT * FROM users WHERE email = :email
""")
        result = db.execute(query, {"email": input.email}).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail = "invalid email or password")
        verified_password = bcrypt.checkpw(input.password.encode("utf-8"), result.password.encode("utf-8"))
        if not verified_password:
            raise HTTPException(status_code=404, detail =" invalid email or password")
        encoded_token = create_token(details = {
            "email": result.email,
            "userType": result.userType,
            "id":result.id
        },expiry = token_time)
        return {
            "message": "Login Successful",
            "token": encoded_token
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail = str(e))
    
    
class courseRequest(BaseModel):
    title: str = Field(..., example="Backend Course")
    level: str = Field(..., example="Beginner")
@app.post("/courses")
def addcourses(input: courseRequest, user_data = Depends(verify_token)):
    try:
        print(user_data)
        if user_data["userType"] != "Admin":
            raise HTTPException(status_code=401, detail="You are not authorized to add a course")
        query = text("""
            INSERT INTO courses (title, level)
            VALUES(:title, :level)
""")
        db.execute(query, {"title": input.title, "level":input.level})
        db.commit()
        return {
            "message": "Course added successfully",
            "data": {
                "title": input.title,
                "level": input.level
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, details=str(e))

# class enrolmentRequest(BaseModel):
#     userId: int = Field(..., example=1)

# @app.post("/enrollments")
# def add_enrollment(input: enrolmentRequest, user_data = Depends(verify_token)):
#     try:
#         print(user_data)
#         if user_data["userType"] != "student":
#             raise HTTPException(status_code=401, detail="You are not authorized to enroll a course")
        

        
#         query = text("""
#             INSERT INTO enrollments (userId, courseId)
#             VALUES(:userId, :courseId)
# """)
#         db.execute(query, {"userId": user_data["userId"], "courseId": input.courseId})
#         db.commit()
#         return {
#             "message": "Enrolled successfully",
#             "data": {
#                 "userId": user_data["userId"],
#                 "courseId": input.courseId
#             }
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, details=str(e))


class EnrollRequest(BaseModel):
    courseId: int = Field(..., example=1)
@app.post("/enroll")
def enrollcourses(input: EnrollRequest, user_data = Depends(verify_token)):
    try:
        print(user_data)
        if user_data["userType"] != "student":
            raise HTTPException(status_code=401, detail="You are not authorized to enroll to a course")
        # Check if user already enrolled
        check_query = text("""
            SELECT * FROM enrollments
            WHERE userId = :userId AND courseId = :courseId
        """)
        existing = db.execute(check_query, {
            "userId": user_data["userId"],
            "courseId": input.courseId
        }).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Already enrolled in this course")
        query = text("""
            INSERT INTO enrollments (userId, courseId)
            VALUES (:userId, :courseId)
        """)
        db.execute(query, {"userId": user_data["userId"], "courseId": input.courseId})
        db.commit()
        return {
            "message": "Course added successfully",
            "data": {"userId": user_data["userId"], "courseId": input.courseId}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__=="__main__":
     uvicorn.run(app,host=os.getenv("host"), port=int(os.getenv("port")))




