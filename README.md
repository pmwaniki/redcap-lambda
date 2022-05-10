# redcap-lambda
AWS lambda function for monitoring REDCap downtime.
The application runs on AWS Lambda functions. There are two lambda functions. One functions is triggered by AWS Cloudwatch every 10 minutes and checks whether the REDCap site is up using 'requests' library and logs the output to a Dynamodb table. The second function can be accessed as a REST API endpoint and fetchs data from the Dynamodb table.


The application can be uploaded using AWS SAM CLI by running 'sam build' and 'sam deploy --guided'. AWS credentials must first be set using 'aws configure'.

The repository also contains github actions and would be build and uploaded to AWS whenever a git push command is run on the main branch. This requires AWS credentials be set up in the github account.