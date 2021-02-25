from typing import List

import databases
import sqlalchemy
from sqlite3 import IntegrityError


class FriendsManager:
    """
    Class for managing friendship relations in database.
    It works only with sqlite database.
    Typical usage:
        Initialization:
            friends_manager = FriendsManager('sqlite:///./sql_db.db')
            friends_manager.create_all()
            await friends_manager.connect()

        Operation:
            friends_manager.add_friends(2, 1)
            friends_manager.get_friends(1)
            friends_manager.remove_friends(2, 1)

        Exiting:
            await friends_manager.disconnect()
    """

    def __init__(self, database_url: str):
        self.database = databases.Database(database_url)
        self.metadata = sqlalchemy.MetaData()

        self.friends = sqlalchemy.Table(
            "friends",
            self.metadata,
            sqlalchemy.Column("user1", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("user2", sqlalchemy.Integer, primary_key=True),
        )

        self.engine = sqlalchemy.create_engine(
            database_url, connect_args={"check_same_thread": False}
        )

    def create_all(self):
        """Creates all tables in database."""
        self.metadata.create_all(self.engine)

    def drop_all(self):
        """Drops all tables in database."""
        self.metadata.drop_all(self.engine)

    async def connect(self):
        """Connects to the database."""
        await self.database.connect()

    async def disconnect(self):
        """Disconnects from the database."""
        await self.database.disconnect()

    async def get_friends(self, user_id: int) -> List[int]:
        """
        Returns list of the user friends.
        Args:
            user_id: Id of the user.

        Returns:
            List of the user friends ids.
        """
        select1 = self.friends.select().with_only_columns([self.friends.c.user1]).where(self.friends.c.user2 == user_id)
        select2 = self.friends.select().with_only_columns([self.friends.c.user2]).where(self.friends.c.user1 == user_id)
        query = select1.union(select2)
        results = await self.database.fetch_all(query)
        return [x[0] for x in results]

    async def add_friends(self, user1: int, user2: int):
        """
        Register friend relationship in database.
        Id of the 1st user must be greater than 2nd to avoid double records in database.
        Args:
            user1: id of the 1st user
            user2: id of the 2nd user
        """
        self.__check_ids_order(user1, user2)
        query = self.friends.insert().values(user1=user1, user2=user2)
        try:
            await self.database.execute(query)
        except IntegrityError:
            pass

    async def remove_friends(self, user1: int, user2: int):
        """
        Delete friend relationship from database.
        Id of the 1st user must be greater than 2nd.
        Args:
            user1: id of the 1st user
            user2: id of the 2nd user
        """
        self.__check_ids_order(user1, user2)
        query = self.friends.delete().where(self.friends.c.user1 == user1 and self.friends.c.user2 == user2)
        await self.database.execute(query)

    def __check_ids_order(self, user1, user2):
        """Checks if ids are in correct order, user1 > user2. If not raises exception."""
        if user1 <= user2:
            raise ValueError('Error, id of the first user should be greater than second user id.')
