

from interfaces.dynamodb_infra import DynamoDBClient
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

from exceptions.custom_exception import UserRepositoryException, DataBaseException

class UserRepository:
    def __init__(self):
        self.__dynamo_client = DynamoDBClient("tb_users")
        self.serializer = TypeSerializer()   
        self.deserializer = TypeDeserializer()
        self.__SIZE_CHUNKS = 25     


    def get_all_users(self):
        try:
            users = self.__dynamo_client.scan_items()
            deserialized_users = [self.__deserialize_item(user) for user in users]
            return self.__aggregate_users(deserialized_users)
        except Exception as e:
            raise DataBaseException("Error getting users") from e
        
    def get_order_by_id(self, user_id, order_id):
        try:
            key_condition = 'user_id = :user_id AND order_id = :order_id'
            expression_attribute_values = {
                ':user_id': {'N': str(user_id)},
                ':order_id': {'N': str(order_id)}
            }
            orders = self.__dynamo_client.get_item_condition(key_condition, expression_attribute_values)
            if orders:
                deserialized_orders = [self.__deserialize_item(order) for order in orders]
                return deserialized_orders[0]
            return None
        except Exception as e:
            raise DataBaseException("Error getting order") from e
        
    def get_user_by_id(self, user_id):
        try:
            key_condition = 'user_id = :user_id'
            expression_attribute_values = {
                ':user_id': {'N': str(user_id)}
            }
            users = self.__dynamo_client.get_item_condition(key_condition, expression_attribute_values)
            if users:
                deserialized_users = [self.__deserialize_item(user) for user in users]
                return self.__aggregate_users(deserialized_users)
            return None
        except Exception as e:
            raise DataBaseException("Error getting user") from e

    
    def __deserialize_item(self, item):
        return {k: self.deserializer.deserialize(v) for k, v in item.items()}
    

    def __aggregate_users(self, users):
        aggregated_users = {}
        for user in users:
            user_id = user["user_id"]
            if user_id not in aggregated_users:
                aggregated_users[user_id] = {
                    "user_id": user_id,
                    "name": user["name"],
                    "orders": []
                }
            aggregated_users[user_id]["orders"].append({
                "order_id": user["order_id"],
                "total": user["total"],
                "products": user["products"],
                "date": user["date"]
            })
        return list(aggregated_users.values())


    def save_users_batch(self, file):
        try:
            users = self.__group_users(file)
            serialized_items = []
            for user in users:
                for order in user.get("orders"):
                    item = {
                        "user_id": user["user_id"],
                        "order_id": order["order_id"],
                        "name": user["name"],
                        "products": order["products"]
                    }
                    serialized_item = {k: self.serializer.serialize(v) for k, v in item.items()}
                    serialized_items.append(serialized_item)
            for chunk in self.__chunked(serialized_items, self.__SIZE_CHUNKS):
                response = self.__dynamo_client.put_item_batch(chunk)
        except Exception as e:
            raise UserRepositoryException("Error saving users") from e


    def __chunked(self, iterable, size):
        """Divide a lista em chunks de tamanho especificado."""
        for i in range(0, len(iterable), size):
            yield iterable[i:i + size]


    def __group_users(self, file) -> dict:
        rows = self.__to_dict(file)
        users = []
        for row in rows:
            user = self.__find_or_create_user(users, row)
            order = self.__find_or_create_order(user, row)
            self.__add_product_to_order(order, row)

        return users

    
    def __find_or_create_user(self, users, row):
        user = next((user for user in users if user["user_id"] == row["user_id"]), None)
        if user is None:
            user = {
                "user_id": row["user_id"],
                "name": row["name"],
                "orders": []
            }
            users.append(user)
        return user
    

    def __find_or_create_order(self, user, row):
        order = next((order for order in user["orders"] if order["order_id"] == row["order_id"]), None)
        if order is None:
            order = {
                "order_id": row["order_id"],
                "total": 0,
                "date": row["purchase_date"],
                "products": []
            }
            user["orders"].append(order)
        return order
    

    def __add_product_to_order(self, order, row):
        product = {
            "product_id": row["product_id"],
            "value": row["product_value"]
        }
        order["products"].append(product)
        order["total"] += float(row["product_value"])


    def __to_dict(self, file)-> dict:
        processed_data = []
        for line in file:
            line = line.decode('utf-8').strip()

            order_data = {
                "user_id": int(line[0:10].strip().lstrip('0')),
                "name": line[10:55].strip(),
                "order_id": int(line[55:65].strip().lstrip('0')),
                "product_id": line[65:75].strip().lstrip('0'),
                "product_value": line[75:87].strip(),
                "purchase_date": line[87:95].strip()
            }

            processed_data.append(order_data)
        return processed_data