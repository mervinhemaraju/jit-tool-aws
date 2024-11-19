data "aws_iam_policy_document" "lambda_iam_policy" {

  statement {
    actions = [
      "secretsmanager:*",
      "scheduler:*",
    ]
    resources = ["*"]
  }
}
