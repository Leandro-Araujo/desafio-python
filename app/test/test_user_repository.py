import unittest
from unittest.mock import MagicMock, patch
from src.repositories.user_repository import UserRepository
from src.exceptions.custom_exception import DataBaseException, UserRepositoryException

class TestUserRepository(unittest.TestCase):

    @patch('repositories.user_repository.DynamoDBClient')
    def setUp(self, MockDynamoDBClient):
        self.mock_dynamo_client = MockDynamoDBClient.return_value
        self.user_repository = UserRepository()

    def test_get_all_users_success(self):
        self.mock_dynamo_client.scan_items.return_value = [
            {'user_id': {'N': '1'}, 'name': {'S': 'John Doe'}, 'order_id': {'N': '101'}, 'total': {'N': '100.0'}, 'products': {'L': []}, 'date': {'S': '2023-01-01'}}
        ]
        users = self.user_repository.get_all_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['user_id'], 1)
        self.assertEqual(users[0]['name'], 'John Doe')

    def test_get_all_users_database_exception(self):
        self.mock_dynamo_client.scan_items.side_effect = Exception("Database error")
        with self.assertRaises(DataBaseException):
            self.user_repository.get_all_users()

    def test_get_user_by_id_success(self):
        self.mock_dynamo_client.get_item_condition.return_value = [
            {'user_id': {'N': '1'}, 'name': {'S': 'John Doe'}, 'order_id': {'N': '101'}, 'total': {'N': '100.0'}, 'products': {'L': []}, 'date': {'S': '2023-01-01'}}
        ]
        user = self.user_repository.get_user_by_id(1)
        self.assertIsNotNone(user)
        self.assertEqual(user[0]['user_id'], 1)
        self.assertEqual(user[0]['name'], 'John Doe')

    def test_get_user_by_id_database_exception(self):
        self.mock_dynamo_client.get_item_condition.side_effect = Exception("Database error")
        with self.assertRaises(DataBaseException):
            self.user_repository.get_user_by_id(1)

    def test_save_users_batch_success(self):
        file = [
            b'0000000001John Doe                         00000001010000000001  00000000010020230101'
        ]
        self.user_repository.save_users_batch(file)
        self.mock_dynamo_client.put_item_batch.assert_called()

    def test_save_users_batch_exception(self):
        file = [
            b'0000000001John Doe                         00000001010000000001  00000000010020230101'
        ]
        self.mock_dynamo_client.put_item_batch.side_effect = Exception("Database error")
        with self.assertRaises(UserRepositoryException):
            self.user_repository.save_users_batch(file)

if __name__ == '__main__':
    unittest.main()
