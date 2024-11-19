
# Terraform configuration
terraform {

  # Backend configuration
  backend "s3" {}

  # Required TF version
  required_version = ">= 1.8.0"

  # Required providers
  required_providers {

    # AWS provider version
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5"
    }
  }
}


# AWS Provider configuration
provider "aws" {

  # Region to deploy to
  region = var.region
}
