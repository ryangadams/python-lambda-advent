# Advent Calendar AWS Lambda

A Lambda function that generates an advent calendar from data stored in Google Sheets.

## Deployment

There's a `makefile` to handle the deployment using cdk.

`make build deploy`

Edit `cdk.json` and put the correct Google Sheet Id and Sheet Range in (range is `Sheet1!A:E`)

Put credentials for a Google Service Account into Secretsmanager that has access to the sheet id. The secret name should be `advent/gdrive-service-credentials` and the json for the credentials stored inside it with the key `gdrive_credentials`

## Code

CDK Code is written in Python and found inside [cdk](cdk) directory.

Lambda code is written in Python and found inside [advent](advent)

Dependencies are managed through Pipenv and can be installed using `pipenv install`

Test coverage is not great, but written in pytest in [tests](tests)