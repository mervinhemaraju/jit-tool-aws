import json
import base64
from boto3 import client
from kink import inject


@inject
class SecretsManager:
    def __init__(self, boto_secretsmanager: client, secrets_name: str) -> None:
        # * Store attributes
        self.boto = boto_secretsmanager
        self.secrets_name = secrets_name

    def retrieve_secrets(self) -> dict:
        get_secret_value_response = self.boto.get_secret_value(
            SecretId=self.secrets_name
        )

        # * Decrypts secret using the associated KMS CMK.
        # * Depending on whether the secret is a string or binary, one of these fields will be populated.
        return json.loads(
            get_secret_value_response["SecretString"]
            if "SecretString" in get_secret_value_response
            else base64.b64decode(get_secret_value_response["SecretBinary"])
        )
