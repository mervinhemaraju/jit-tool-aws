"""
OKTA class for managing users
"""

import requests
import logging
from kink import inject
from it_okta.exceptions import OktaUserNotFound


@inject
class User:
    """
    Okta User Class
    """

    def __init__(self, okta_endpoint, okta_api_key, timeout=5) -> None:
        self.prefix = f"{okta_endpoint}/api/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"SSWS {okta_api_key}",
        }
        self.timeout = timeout

    def find_user(self, email: str):
        """
        Find a user by email
        """

        # Make the API call
        response = requests.get(
            f"{self.prefix}/users?q={email}&limit=1",
            headers=self.headers,
            timeout=self.timeout,
        )

        # Check for errors
        response.raise_for_status()

        # Retrieve the users
        users = response.json()

        # Log info
        logging.info(f"Found {len(users)} users with email {email}")

        # Verify if user is present
        if len(users) > 0:
            return users[0]

        # ! Raise an exception if not
        raise OktaUserNotFound(f"User {email} not found in Okta.")
