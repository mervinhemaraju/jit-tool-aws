"""
Okta Group
"""

import logging
import requests
from kink import inject


@inject
class Group:
    """
    Okta Group Class
    """

    def __init__(self, okta_endpoint, okta_api_key, group_name, timeout=5) -> None:
        self.endpoint = okta_endpoint
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"SSWS {okta_api_key}",
        }
        self.group_name = group_name
        self.timeout = timeout
        self.group_id = self.get_okta_group_id()

    def get_okta_group_id(self):
        """
        Get a group ID from an Okta Group Name
        """

        response = requests.get(
            f"{self.endpoint}/api/v1/groups?q={self.group_name}",
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()

        groups_response = response.json()

        if len(groups_response) > 1:
            logging.warning(
                f"More than 1 group was found that matched the filter {self.group_name}"
            )
            for group_id_response in groups_response:
                if group_id_response["profile"]["name"] == self.group_name:
                    return group_id_response["id"]
            logging.warning(
                f"No matching results found for {self.group_name}. Returning None."
            )
            return None

        if len(groups_response) < 1:
            logging.warning(
                f"No results returned for {self.group_name}. Returning None."
            )
            return None

        return groups_response[0]["id"]

    def add_user(self, user_id):
        """
        Okta Add User
        """

        logging.info(f"Adding user with ID {user_id} to Okta Group {self.group_id}")

        user_add_response = requests.put(
            f"{self.endpoint}/api/v1/groups/{self.group_id}/users/{user_id}",
            headers=self.headers,
            timeout=self.timeout,
        )

        logging.info(f"Status Code: {user_add_response.status_code}")

        if user_add_response.status_code != 204:
            logging.error("Error adding okta users to a group using the API")
            logging.exception("Error adding okta users in a group using the API")
            user_add_response.raise_for_status()

        logging.info(
            f"Successfully added user with ID: {user_id} to group {self.group_id}"
        )

    def remove_user(self, user_id):
        """
        Okta Remove User
        """

        logging.info(f"Removing user with ID {user_id} from Okta Group {self.group_id}")

        user_add_response = requests.delete(
            f"{self.endpoint}/api/v1/groups/{self.group_id}/users/{user_id}",
            headers=self.headers,
            timeout=self.timeout,
        )

        logging.info(f"Status Code: {user_add_response.status_code}")

        if user_add_response.status_code != 204:
            logging.error(
                f"Error removing okta user {user_id} from a group using the API"
            )
            logging.exception(
                f"Error removing okta user {user_id} from a group using the API"
            )
            user_add_response.raise_for_status()

        logging.info(
            f"Successfully removed user with ID: {user_id} from the group {self.group_id}"
        )
