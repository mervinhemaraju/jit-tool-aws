import os
from kink import di
from functools import wraps
from boto3 import Session
from botocore.config import Config
from models.aws.secrets_manager import SecretsManager


def main_injection(func):
    def __build_boto_client(client_name, config):
        return Session().client(service_name=client_name, config=config)

    @wraps(func)
    def wrapper(*args, **kwargs):
        # * DI for os variables
        di["env"] = os.environ["ENVIRONMENT"]
        di["aws_region"] = os.environ["AWS_REGION"]
        di["secrets_okta_name"] = os.environ["SECRETS_OKTA_NAME"]
        di["okta_endpoint"] = os.environ["OKTA_ENDPOINT"]
        di["schedule_group"] = os.environ["ACCESS_REQUEST_SCHEDULE_GROUP"]

        # * Boto3 variables
        di["boto_config"] = Config(region_name=di["aws_region"], signature_version="v4")

        di["boto_secretsmanager"] = __build_boto_client(
            client_name="secretsmanager", config=di["boto_config"]
        )
        di["boto_scheduler"] = __build_boto_client(
            client_name="scheduler", config=di["boto_config"]
        )

        # Get the secrets for Okta
        di["secrets_okta"] = SecretsManager(
            secrets_name=di["secrets_okta_name"],
        ).retrieve_secrets()

        # Define api keys
        di["okta_api_key"] = di["secrets_okta"]["api_key"]

        func(*args, **kwargs)

    return wrapper
