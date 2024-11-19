module "lambda_iam_policy" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-policy"
  version = "~> 5"

  name = "${local.service}-iam-policy"
  path = "/"

  policy = data.aws_iam_policy_document.lambda_iam_policy.json
}
