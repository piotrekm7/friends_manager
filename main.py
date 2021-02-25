from typing import List
import os

from fastapi import FastAPI, Depends

from models import Relationship
from friends_manager import FriendsManager


app = FastAPI()


async def get_friends_manager():
    friends_manager = FriendsManager(os.environ.get('DB_URL'))
    friends_manager.create_all()
    await friends_manager.connect()
    try:
        yield friends_manager
    finally:
        await friends_manager.disconnect()


@app.get("/friends/{user_id}", response_model=List[int])
async def friends(user_id: int, friends_manager: FriendsManager = Depends(get_friends_manager)):
    return await friends_manager.get_friends(user_id)


@app.post("/add_friends/")
async def add_friends(relationship: Relationship, friends_manager: FriendsManager = Depends(get_friends_manager)):
    return await friends_manager.add_friends(relationship.user1, relationship.user2)


@app.post("/remove_friends/")
async def remove_friends(relationship: Relationship, friends_manager: FriendsManager = Depends(get_friends_manager)):
    return await friends_manager.remove_friends(relationship.user1, relationship.user2)
