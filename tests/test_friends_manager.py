import os

from aiounittest import AsyncTestCase

from friends_manager import FriendsManager



class TestFriendsManager(AsyncTestCase):

    def setUp(self):
        self.friends_manager = FriendsManager(os.environ.get('TEST_DB'))
        self.friends_manager.create_all()
        self.friends_manager.connect()

    def tearDown(self):
        self.friends_manager.disconnect()
        self.friends_manager.drop_all()

    async def test_adding_and_reading_friends(self):
        await self.friends_manager.add_friends(1, 0)
        await self.friends_manager.add_friends(2, 0)

        self.assertListEqual(await self.friends_manager.get_friends(0), [1, 2])
        self.assertListEqual(await self.friends_manager.get_friends(1), [0])
        self.assertListEqual(await self.friends_manager.get_friends(2), [0])

    async def test_adding_same_friendship_twice(self):
        await self.friends_manager.add_friends(1, 0)
        await self.friends_manager.add_friends(1, 0)

        self.assertListEqual(await self.friends_manager.get_friends(0), [1])
        self.assertListEqual(await self.friends_manager.get_friends(1), [0])

    async def test_incorrect_id_order_raises_exception(self):
        with self.assertRaises(ValueError):
            await self.friends_manager.add_friends(0, 1)
        with self.assertRaises(ValueError):
            await self.friends_manager.remove_friends(0, 1)

    async def test_removing_friends(self):
        await self.friends_manager.add_friends(1, 0)
        self.assertListEqual(await self.friends_manager.get_friends(0), [1])
        self.assertListEqual(await self.friends_manager.get_friends(1), [0])

        await self.friends_manager.remove_friends(1, 0)
        self.assertListEqual(await self.friends_manager.get_friends(0), [])
        self.assertListEqual(await self.friends_manager.get_friends(1), [])
