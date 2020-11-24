import json
import os
import pathlib

import boto3
from botocore.exceptions import ClientError
from google.oauth2 import service_account

scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def fetch_credentials():
    def get_local_credentials():
        secret_file = pathlib.Path(
            pathlib.Path(__file__).parent.absolute()
            / ".."
            / ".."
            / "google-creds.json",
        ).resolve()
        return service_account.Credentials.from_service_account_file(
            secret_file, scopes=scopes
        )

    def get_secret_credentials():
        secret_name = os.environ.get("GDRIVE_CREDENTIALS_SECRET")
        region = os.environ.get("AWS_REGION")
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region)

        try:
            secret_value = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                print("The requested secret " + secret_name + " was not found")
            elif e.response["Error"]["Code"] == "InvalidRequestException":
                print("The request was invalid due to:", e)
            elif e.response["Error"]["Code"] == "InvalidParameterException":
                print("The request had invalid params:", e)
            raise e
        else:
            if "SecretString" in secret_value:
                secret_data = secret_value["SecretString"]
            else:
                secret_data = secret_value["SecretBinary"]
            secret_data = json.loads(secret_data)
            return service_account.Credentials.from_service_account_info(
                json.loads(secret_data["gdrive_credentials"])
            )

    if os.environ.get("AWS_EXECUTION_ENV") is None:
        credentials = get_local_credentials()
    else:
        credentials = get_secret_credentials()
    return credentials


credentials = fetch_credentials()


def get_credentials():
    global credentials
    if credentials is None:
        print("no cached credentials, fetching from secrets manager")
        credentials = fetch_credentials()
    return credentials
