
# JIT Tool for Time-Based Okta Group Management

This repository contains a **Just-In-Time (JIT) Tool** built using **AWS Lambda** and **AWS EventBridge Schedulers** to automate the addition and removal of users from Okta groups based on predefined schedules.

## Features

- **Time-Based User Management**: Automatically adds or removes users from Okta groups at specified times.
- **Serverless Architecture**: Fully implemented using AWS Lambda for scalability and cost-efficiency.
- **Flexible Scheduling**: Utilize AWS EventBridge Schedulers for precise, configurable triggers.
- **Integration with Okta API**: Seamless interaction with Okta's group and user management functionalities.

## How It Works

1. **Define Schedules**:
   - Use AWS EventBridge to create schedules that trigger Lambda functions at specific times.
   
2. **Lambda Functions**:
   - **Add Users**: A Lambda function to add users to specified Okta groups.
   - **Remove Users**: A Lambda function to remove users from specified Okta groups.

3. **Okta API Integration**:
   - The tool communicates with the Okta API to perform group management tasks based on the provided user data and group configurations.

## Prerequisites

- **AWS Account** with permissions to manage Lambda, EventBridge, and IAM roles.
- **Okta API Token** with sufficient permissions for user and group management.
- **Python Runtime** (depending on the Lambda implementation).

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/jit-okta-tool.git
   cd jit-okta-tool
   ```

2. **Deploy to AWS**:
    Use the AWS CLI or a deployment tool like AWS SAM or Serverless Framework to deploy the Lambda functions and configure EventBridge schedules.

3. **Configure Okta**:
    Set up the API token in AWS Secrets Manager.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to improve this tool.
