import json
import copy
from datetime import datetime
from models.others.event import Event
from models.aws.scheduler import Scheduler
from models.okta.group import Group as OktaGroup
from models.okta.user import User as OktaUser


def add_to_okta_group(group_name: str, requester_email: str):
    # Instantiate the okta user class
    user = OktaUser()

    # Find the user id on okta
    user_id = user.find_user(requester_email)["id"]

    # Instantiate the okta group class
    group = OktaGroup(group_name=group_name)

    # Add the user to the group
    group.add_user(user_id)


def remove_from_okta_group(group_name: str, requester_email: str):
    # Instantiate the okta user class
    user = OktaUser()

    # Find the user id on okta
    user_id = user.find_user(requester_email)["id"]

    # Instantiate the okta group class
    group = OktaGroup(group_name=group_name)

    # Remove the user from the group
    group.remove_user(user_id)


def create_scheduler(event: Event, at: datetime, target_arn: str, role_arn: str):
    # Create a scheduler object
    scheduler = Scheduler()

    # Convert the datetime to string at(yyyy-mm-ddThh:mm:ss)
    at = at.strftime("%Y-%m-%dT%H:%M:%S")

    # Create an export of the value
    input = (copy.deepcopy(event)).export()

    # Retrieve the requester username
    user_name = event.retrieve_requester_username()

    # Create the schedule
    scheduler.create_schedule(
        name=f"{event.event_type.value}-access-{user_name}-okta-{event.ticket_id}",
        description=f"This scheduler will {event.event_type.value} access for the user {event.requester_email} in Okta against the group {event.okta_group_name}.",
        schedule_expression=f"at({at})",
        target={
            "Arn": target_arn,
            "RoleArn": role_arn,
            "Input": json.dumps(input),
        },
        action_after_complete="DELETE",
    )
