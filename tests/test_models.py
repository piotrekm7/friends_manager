from unittest import TestCase

from models import Relationship


class TestRelationship(TestCase):

    def test_user1_is_always_greater_id(self):
        user1, user2 = 1, 2

        relation1 = Relationship(user1, user2)
        relation2 = Relationship(user2, user1)

        self.assertEqual(relation1.user1, 2)
        self.assertEqual(relation2.user1, 2)

    def test_negative_id_raises_exception(self):
        with self.assertRaises(ValueError):
            Relationship(-1, 1)
        with self.assertRaises(ValueError):
            Relationship(1, -1)

    def test_same_ids_raises_exception(self):
        with self.assertRaises(ValueError):
            Relationship(5, 5)
