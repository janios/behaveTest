from behave import given, when, then
from features.utils import secrets
import os
import uuid
import json
from features.utils.rpc_client import RpcClient
from datetime import date
from features.utils.dao import LedgerDAO


@given('Environment, region, secret, stack and queue "{queue}"')
def step_impl(context, queue):
    rabbit_port = 5671
    region = os.environ.get("REGION")
    profile = os.environ.get("PROFILE", None)
    env = os.environ.get("ENVIRONMENT")
    stack = os.environ.get("STACK")
    s_secret_container = os.environ.get("SECRET_CONTAINER", None)
    print(s_secret_container)
    if s_secret_container is None:
        secret = f'/{env}/rmq/service-ap-journal/1'
        rabbit_config = json.loads(secrets.get_ssm(secret, region, profile))
        rabbit_username = rabbit_config['username']
        rabbit_password = rabbit_config['password']
    else:
        secret_container = json.loads(s_secret_container)
        rabbit_username = secret_container['username']
        rabbit_password = secret_container['username']
    endpoint = f'/{env}/rabbitmq/ledger/{stack}/endpoint'
    rabbit_hostname = secrets.get_ssm(endpoint, region, profile)
    rpc_client = RpcClient(rabbit_username, rabbit_password, rabbit_hostname, rabbit_port)
    context.rpcClient = rpc_client
    context.queue = queue


@when('I create a journal movement with account id "{account_id}", source type "{src_type}", movement type "{mvnt_type}", and amount "{amount}"')
def send_journal_message(context, account_id, src_type, mvnt_type, amount):
    context.accountId = account_id
    today = date.today()
    movement = {
        'account_type': 'M',
        'account_id': account_id,
        'source_type': src_type,
        'movement_type': mvnt_type,
        'effective_date': {"date": today.strftime("%Y-%m-%d"),
                           "time": {"hour": 00, "minute": 00, "second": 52, "nano": 0}},
        "movement_date": {"date": today.strftime("%Y-%m-%d"),
                          "time": {"hour": 00, "minute": 00, "second": 00, "nano": 0}},
        'amount': str(amount),
        'currency': 'MXN',
        'movement_id': str(uuid.uuid1())
    }
    message = {'movement': movement}
    response = context.rpcClient.call(json.dumps(message), context.queue)
    context.response = json.loads(response)
    print(response)


@when('I create a frozen balance in the "{set_frozen_queue}" with source type "{frozen_src_type}", movement type "{frozen_movement_type}" and amount "{frozen_amount}"')
def send_frozen_balance(context, set_frozen_queue, frozen_src_type, frozen_movement_type, frozen_amount ):
    frozen_movement = {
        'account_type': 'M',
        'account_id': context.accountId,
        'source_type': frozen_src_type,
        'movement_type': frozen_movement_type,
        'amount': str(frozen_amount),
        'currency': 'MXN'
    }
    message = {'frozen_balance': frozen_movement}
    print("Message ", message)
    response = context.rpcClient.call(json.dumps(message), set_frozen_queue)
    context.response = json.loads(response)
    context.frozeId = context.response['frozen_id']
    print("Response ", response)
    print("Frozen Id", context.frozeId)


@when('I release a frozen balance in the "{release_frozen_queue}"  with source type "{frozen_src_type}" and "{frozen_movement_type}"')
def send_release_frozen_balance(context, release_frozen_queue, frozen_src_type, frozen_movement_type):
    frozen_movement = {
        'account_type': 'M',
        'account_id': context.accountId,
        'source_type': frozen_src_type,
        'movement_type': frozen_movement_type,
        'frozen_id': context.frozeId
    }
    message = {'release_frozen_balance': frozen_movement}
    response = context.rpcClient.call(json.dumps(message), release_frozen_queue)
    context.response = json.loads(response)
    print("Response ", response)


@then('The response status must be "{status}"')
def response_status(context, status):
    print("Response ", context.response["status"])
    assert context.response["status"] == status


@then('In dynamo table "{frozen_balance_table}" for the environment "{env}" with source type "{frozen_src_type}", movement type "{frozen_movement_type}"  the status must be "{frozen_balance_status}"')
def frozen_balance_table_status(context, frozen_balance_table, env, frozen_src_type, frozen_movement_type, frozen_balance_status ):
    frozen_balance_item = LedgerDAO(env, frozen_balance_table).find_ledger_balance(context.accountId, frozen_src_type, frozen_movement_type, context.frozeId)
    print("Frozen Balance ", frozen_balance_item )
    assert frozen_balance_status == frozen_balance_item['status']






