module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 7"

  function_name = "${local.service}-${var.env}"
  description   = "Lambda function for the ${local.service} service"

  architectures = ["x86_64"]
  handler       = "main.main"
  runtime       = "python3.11"

  memory_size                       = 128
  cloudwatch_logs_retention_in_days = 90
  reserved_concurrent_executions    = 15
  timeout                           = 300

  tracing_mode = "Active"

  assume_role_policy_statements = {
    AllowSchedulerAssumptions = {
      effect  = "Allow",
      actions = ["sts:AssumeRole"],
      principals = {
        service_principal = {
          type        = "Service"
          identifiers = ["scheduler.amazonaws.com"]
        }
      }
    }
  }

  create_role                   = true
  role_name                     = "${local.service}-${var.env}"
  policy                        = module.lambda_iam_policy.arn
  attach_policy                 = true
  attach_cloudwatch_logs_policy = true
  attach_network_policy         = true
  attach_tracing_policy         = true

  layers = local.configs.datadog.layer_extensions

  publish = true

  source_path = "./function"

  environment_variables = {
    ENVIRONMENT                   = var.env
    SECRETS_OKTA_NAME             = local.configs.secrets.okta_name
    OKTA_ENDPOINT                 = var.okta_domain
    ACCESS_REQUEST_SCHEDULE_GROUP = local.constants.scheduler.group.access_requests.name
  }

}
