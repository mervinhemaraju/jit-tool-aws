variable "region" {
  type        = string
  description = "The AWS region to deploy the resources to."
}

variable "env" {
  type        = string
  description = "The environment to deploy the resources to."
}

variable "okta_domain" {
  type        = string
  description = "The Okta domain to use for the Okta service."
}
