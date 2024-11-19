"""
Class for EventBridge Scheduler
"""

from boto3 import client
from kink import inject


@inject
class Scheduler:
    """
    Class for EventBridge Scheduler
    """

    def __init__(self, boto_scheduler: client, schedule_group: str = None) -> None:
        """
        Init Method
        """
        self.boto = boto_scheduler
        self.schedule_group = schedule_group

    def create_schedule(
        self,
        name,
        description,
        schedule_expression,
        target,
        action_after_complete="NONE",
        flexible_time_window={"Mode": "OFF"},
        schedule_expression_timezone="UTC",
        state="ENABLED",
    ):
        return self.boto.create_schedule(
            ActionAfterCompletion=action_after_complete,
            Description=description,
            FlexibleTimeWindow=flexible_time_window,
            GroupName=self.schedule_group,
            Name=name,
            ScheduleExpression=schedule_expression,
            ScheduleExpressionTimezone=schedule_expression_timezone,
            State=state,
            Target=target,
        )
