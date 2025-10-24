from database import DatabaseConnection
from fastapi import FastAPI
from pydantic import basemodel, field_serializer   
from sqlalchemy import text
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()
app = FastAPI( title="Simple App", version="1.0")

class Simple(basemodel):
    name: str= Field(..., example="Oludayo")
    id: int = Field(..., example=1)
    username: str = Field(..., example="oludayo123")
    email: str = Field(..., example="oludayo@example.com")
    age: int = Field(..., example=30)
    location: str = Field(..., example="Nigeria")
    password: str = Field(..., example="securepassword")

    @app.post("/signup")
    def signUp(input: Simple):
        try:
            query = text("""
                INSERT INTO user (username, email, age, location, password)
                VALUES (:username, :email, :age, :location, :password)
            """)

            salt=bcrypt.gensalt()
            hashedpassword =bcrypt.hashpw(input.password.encode('utf-8'), salt)
            print(hashedpassword)
            db.execute(query, {
                "username": input.username,
                "email": input.email,
                "age": input.age,
                "location": input.location,
                "password": input.password
            })
        return {"message": "User created successfully",
                "data": {"username": input.username,
                          "email": input.email,
                          "age": input.age,
                          "location": input.location,
                          "password": input.password}
               }

db_connection = DatabaseConnection()
