from core.request_type import RequestType


class Event:
    def __init__(self, event) -> None:
        self.is_emergency = event["is_emergency"].lower()
        self.requester_email = event["requester_email"]
        self.ticket_id = event["ticket_id"]
        self.okta_group_name = event["okta_group_name"]
        self.event_type: RequestType = self.__retrieve_event_type(event["event_type"])
        self.duration_in_hours = self.__retrieve_duration(event["duration"])
        self.start_datetime_str = event["start_date_time"]

    def __retrieve_event_type(self, event_type):
        return (
            RequestType(event_type.lower())
            if self.is_emergency == "no"
            else RequestType.ADD
        )

    def __retrieve_duration(self, duration):
        return (
            int(duration.replace("h", "").strip()) if self.is_emergency == "no" else 12
        )

    def retrieve_requester_username(self):
        return self.requester_email.split("@")[0]

    def export(self):
        # Create a dict of the vars
        export = vars(self)

        # Replace the event_type with the value
        export["event_type"] = self.event_type.value

        # Return export
        return export
