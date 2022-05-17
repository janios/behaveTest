# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developers/getting-started/python/

import boto3
from botocore.exceptions import ClientError


def get_ssm(secret_name, region_name, profile_name):

    session = boto3.session.Session(profile_name=profile_name) if profile_name is not None else boto3.session.Session()
    client = session.client(
        service_name='ssm',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_parameter(
            Name=secret_name,
            WithDecryption=True
        )
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif error_code == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif error_code == 'InvalidParameterException':
            print("The request had invalid params:", e)
        else:
            print("Unknown scenario found", e)
        return None
    else:
        return get_secret_value_response['Parameter']['Value']
