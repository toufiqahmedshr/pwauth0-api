from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
    users.append({"username": username, "password": password})
    return {"status": "user created"}

# User Register
@app.get("/users", tags=["auth0"])
def get_users():
    return users


# User Login
@app.post("/users/login", tags=["auth0"])
def user_login(username: str, password: str):
    for user in users:
        if user["username"] == username and user["password"] == password:
            return {"status": "user logged in"}
        else:
            raise HTTPException(status_code=401, detail="username or password did not match")


