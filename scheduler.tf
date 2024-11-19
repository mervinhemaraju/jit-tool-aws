# Create a schedule group for the access requests
resource "aws_scheduler_schedule_group" "access_requests" {
  name = local.constants.scheduler.group.access_requests.name
}
