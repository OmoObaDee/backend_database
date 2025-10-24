from database import db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import bcrypt
import uvicorn

load_dotenv()

app = FastAPI(title="Simple App", version="1.0.0")

class Simple(BaseModel):
    name: str = Field(..., example="Sam Larry")
    email: str = Field(..., example="sam@email.com")
    passord: str = Field(..., example="sam123")
    age: int = Field(..., example=30)

@app.post("/signup")
def signUp(input: Simple):
    try:

        duplicate_query=text("""
            SELECT * FROM user
            WHERE email = :email;
                             """)
        existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
        if existing:
            print("Email already exists")
            # raise HTTPException(status_code=400, detail="Email already exists")


        query = text("""
            INSERT INTO user (name, email, passord, age)
            VALUES (:name, :email, :passord, :age);
        """)

        salt = bcrypt.gensalt()
        hashedpassord = bcrypt.hashpw(input.passord.encode('utf-8'), salt)
        print(hashedpassord)

        db.execute(query, {"name": input.name, "email": input.email, "passord": hashedpassord, "age": 27})
        db.commit()

        return {"message": "User created successfully",
                "data": {"name": input.name, "email": input.email, "passord": input.passord, "age": input.age}}

    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))
    
class longRequest(BaseModel):
    email: str=Field(..., examples="oludayo@email.com")
    password: str=Field(..., examples="oludayo123")

@app.post("/input")
def login(input: longRequest):
    try:
        query= text("""
        SELECT
        * from user
        where email = :email
        """)
        result = db.execute(query, {'email': input.email}).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail = " Invail email or passowrd")
        verified_password= bcrypt.checkpw(input.password.encode('utf-8'), result['password'])
   
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))

class longRequest(BaseModel):
    email: str=Field(..., examples="oludayo@email.com")
    password: str=Field(..., examples="oludayo123") 

    



if __name__=="__main__":
    uvicorn.run(app,host=os.getenv("host"), port=int(os.getenv("port")))