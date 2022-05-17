import os
import boto3
from boto3.dynamodb.conditions import Key, Attr


class DDBConnection:
    table = None

    # DYNAMODB METHODS
    def get_dynamo_table(self):
        dynamodb = boto3.resource('dynamodb')
        return dynamodb.Table(self.table)

    def __init__(self, table_name):
        self.table = table_name


class LedgerDAO:
    ddb_conn = None
    
    def __init__(self, env, table_name):
        print("Table ", f'{env}_{table_name}')
        self.ddb_conn = DDBConnection(f'{env}_{table_name}').get_dynamo_table()

    def find_ledger_balance(self, acct_id, source_type, movement_type, frozen_id):
        balance_item = None
        try:
            print("acct_id ", f'M#{acct_id}')
            balance_item = self.ddb_conn.query(
                KeyConditionExpression=Key('acct_id').eq(f'M#{acct_id}')
                                        & Key('frozen_id').eq(f'{source_type}#{movement_type}#{frozen_id}'))
            print(balance_item)
            balance_item = balance_item["Items"][0] if balance_item["Count"] == 1 else None
        except Exception as e:
            print("[find_ledger_balance] Error while getting balance record: %s", e)
        return balance_item


