import os
from unittest import TestCase

from fastapi.testclient import TestClient

from friends_manager import FriendsManager
from main import app, get_friends_manager


async def override_get_friends_manager():
    friends_manager = FriendsManager(os.environ.get('TEST_DB'))
    friends_manager.create_all()
    await friends_manager.connect()
    try:
        yield friends_manager
    finally:
        await friends_manager.disconnect()


app.dependency_overrides[get_friends_manager] = override_get_friends_manager

client = TestClient(app)


class TestApi(TestCase):
    def test_api_integration(self):
        response = client.get('/friends/0')
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json(), [])

        response = client.post('/add_friends/', json={"user1": 1, "user2": 0})
        self.assertEqual(response.status_code, 200)

        response = client.get('/friends/0')
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json(), [1])

        response = client.post('/remove_friends/', json={"user1": 1, "user2": 0})
        self.assertEqual(response.status_code, 200)

        response = client.get('/friends/0')
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json(), [])
