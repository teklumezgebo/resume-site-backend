# Resume Site — Backend

Serverless visitor counter for [teklu.me](https://teklu.me)

## Architecture

```
Browser (script.js)
      │
      ▼
API Gateway (REST API, CORS enabled)
      │
      ▼
AWS Lambda (Python, boto3)
      │
      ▼
DynamoDB (on-demand, single counter item)
```

Every page load calls the API Gateway endpoint, which invokes a Lambda function
that atomically increments a counter stored in DynamoDB and returns the new value.

## Tech stack

- **AWS Lambda** — Python 3.12, handles the increment logic
- **Amazon DynamoDB** — on-demand billing, single-table counter storage
- **Amazon API Gateway** — REST API, CORS-enabled, proxies requests to Lambda
- **pytest + moto** — unit tests with mocked AWS services, no real infrastructure touched

## Project structure

```
backend/
├── lambda_function.py          # Lambda handler
├── requirements.txt            # runtime + dev dependencies
├── tests/
│   ├── test_lambda_function.py
│   └── test_lambda_function_extended.py
├── .github/workflows/deploy.yml
└── README.md
```

## Running tests locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
```

Tests use `moto` to mock DynamoDB — no real AWS resources are created or modified
when running the test suite.

## Deployment

Pushes to `main` trigger a GitHub Actions workflow that runs the test suite and,
if it passes, deploys the updated code to the live Lambda function.

## What this project demonstrates

- Serverless architecture (API Gateway → Lambda → DynamoDB)
- Least-privilege IAM policies scoped to specific resources
- Infrastructure as code with Terraform, including importing manually-provisioned
  resources into Terraform state
- Automated testing with mocked AWS services
- CI/CD via GitHub Actions

## Related

- Frontend repo: 
- Live site: [teklu.me](https://teklu.me)