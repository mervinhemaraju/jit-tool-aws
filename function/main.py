import logging
from dateutil import parser
from core.di import main_injection
from models.others.event import Event
from core.request_type import RequestType
from core.functions import add_to_okta_group, remove_from_okta_group, create_scheduler
from helpers.utils import calculate_end_datetime

# Set logging level
logging.getLogger().setLevel(logging.INFO)


@main_injection
def main(event, context):
    # TODO(wrap with error handling)
    # Log event and context
    logging.info(f"JIT provisioner started with {event} and context {context}")

    # Create an event class
    event_class = Event(event=event)

    # Log info
    logging.info(f"Request type has been identified as {event_class.event_type.value}")

    # Parse string start_datetime to datetime object
    start_datetime = parser.parse(event_class.start_datetime_str).replace(tzinfo=None)

    # Get the end datetime
    end_datetime = calculate_end_datetime(
        start_datetime=start_datetime, duration_in_hours=event_class.duration_in_hours
    )

    # Gather data
    lambda_function_arn = context.invoked_function_arn
    account_id = lambda_function_arn.split(":")[4]
    role_arn = f"arn:aws:iam::{account_id}:role/{context.function_name}"

    # Log infos
    logging.info(f"Start datetime has been parsed to {start_datetime}")
    logging.info(f"End datetime has been parsed to {end_datetime}")
    logging.info(
        f"Duration in hours has been calculated to {event_class.duration_in_hours}"
    )
    logging.info(f"Origin account ID is {account_id}")
    logging.info(f"Role ARN of the lambda is {role_arn}")

    match event_class.event_type:
        case RequestType.SCHEDULE:
            # Log info
            logging.info("SCHEDULE event triggerred...")

            # Reset event type to ADD
            event_class.event_type = RequestType.ADD

            # Create the schedule
            create_scheduler(
                event=event_class,
                at=start_datetime,
                target_arn=context.invoked_function_arn,
                role_arn=role_arn,
            )

        case RequestType.ADD:
            # Log info
            logging.info("ADD event triggerred...")

            # Add the user to the okta group
            add_to_okta_group(
                group_name=event_class.okta_group_name,
                requester_email=event_class.requester_email,
            )

            # Reset event type to REVOKE
            event_class.event_type = RequestType.REVOKE

            # Create the schedule
            create_scheduler(
                event=event_class,
                at=end_datetime,
                target_arn=context.invoked_function_arn,
                role_arn=role_arn,
            )

        case RequestType.REVOKE:
            # Log info
            logging.info("REVOKE event triggerred...")

            # Remove the user from the okta group
            remove_from_okta_group(
                group_name=event_class.okta_group_name,
                requester_email=event_class.requester_email,
            )

    # TODO(Return something more meaningful)
    return "OK", 200
