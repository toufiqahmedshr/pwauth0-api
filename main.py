from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
from decouple import config


ALG0 = config("algorithm")
KEY0 = config("private_key")

users = []

app = FastAPI()

# Server Test
@app.get("/", tags=["test"])
def test():
    return {
        "server": "test-server",
        "status": "running"
    }


# Create/Add User
@app.post("/users", tags=["auth0"])
def create_user(username: str, password: str):
    user_cred = {
        "username": username,
        "password": password
    }
    enc_user_cred = jwt.encode(user_cred, KEY0, algorithm=ALG0)
    user = {
        "username": username,
        "user_cred": enc_user_cred
    }
    users.append(user)
    return {"status": "user created"}

# User Register
@app.get("/users", tags=["auth0"])
def get_users():
    return users


# User Login
@app.post("/users/login", tags=["auth0"])
def user_login(username: str, password: str):
    for user in users:
        if user["username"] == username:
            user_cred = jwt.decode(user["user_cred"], KEY0, algorithms=[ALG0])
            if user_cred["username"] == username and user_cred["password"] == password:
                return {"status": "user credentials matched"}
            else:
                raise HTTPException(status_code=401, detail="user credentials did not match")
        else:
            return {"status": "user not found"}

