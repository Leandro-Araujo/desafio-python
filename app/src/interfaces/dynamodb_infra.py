import boto3

class DynamoDBClient:
    def __init__(self, table_name):
        self.table_name = table_name
        self.client = boto3.client('dynamodb', 
                                   endpoint_url='http://localhost:4566')


    def get_item(self, key):
        response = self.client.get_item(
            TableName=self.table_name,
            Key=key
        )
        return response.get('Item')
    

    def get_item_condition(self, key_condition, expression_attribute_values):
        response = self.client.query(
            TableName=self.table_name,
            KeyConditionExpression=key_condition,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response.get('Items', [])    

    
    def scan_items(self):
        paginator = self.client.get_paginator('scan')
        items = []
        for page in paginator.paginate(TableName=self.table_name):
            items.extend(page['Items'])
        return items
    

    def put_item(self, item):
        response = self.client.put_item(
            TableName=self.table_name,
            Item=item
        )
        return response
    

    def put_item_batch(self, items):
        response = self.client.batch_write_item(
            RequestItems={
                self.table_name: [
                    {'PutRequest': {'Item': item}} for item in items
                ]
            }
        )
        return response
    

    def delete_item(self, key):
        response = self.client.delete_item(
            TableName=self.table_name,
            Key=key
        )
        return response


    def update_item(self, key, update_expression, expression_attribute_values):
        response = self.client.update_item(
            TableName=self.table_name,
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response