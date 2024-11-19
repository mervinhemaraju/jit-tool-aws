locals {
  service = "okta-jit-provisioning"

  constants = {
    scheduler = {
      group = {
        access_requests = {
          name = "okta-jit-schedulers-requests"
        }
      }
    }
  }

  configs = {

    secrets = {
      okta_name = "secrets/${var.env}/okta/credentials"
    }

  }
}
