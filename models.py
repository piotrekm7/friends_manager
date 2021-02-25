from pydantic import BaseModel, validator, root_validator


class Relationship(BaseModel):
    """
    Friendship relation model.

    Model always stores highest id as the first user.
    Ids must be different non negative integers.
    Args:
        user1: id of the first user
        user2: id of the second user
    """
    user1: int
    user2: int

    def __init__(self, user1: int, user2: int):
        if user1 < user2:
            user1, user2 = user2, user1

        super().__init__(user1=user1, user2=user2)

    @validator('user1', 'user2')
    def id_cannot_be_negative(cls, v):
        """Validates if ids are not negative numbers."""

        if v < 0:
            raise ValueError('User id must be positive value.')
        return v

    @root_validator
    def user_ids_cannot_be_the_same(cls, values):
        """Validates if ids differs, user cannot be self friend."""

        if values.get('user1') == values.get('user2'):
            raise ValueError('User ids for friend relationship cannot be the same.')
        return values
