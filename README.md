# python.ledger-qa-automation
python.ledger-qa-automation owned by team-settlement

## Prerequisites

Install behave with:

```bash
    pip install behave
    pip install behave-html-formatter
```



To run locally is mandatory add environment variables with the following commands:

```bash
    export REGION="us-west-2"
    export PROFILE="dev-team-ledger-assume-role"
    export STACK="a"
    export ENVIRONMENT="dev"
```

## Getting Started
run the features with the following command

```bash
python3 call_behave.py
```



