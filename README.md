# A simple backup script for AWS buckets

This simple scripts uploads the contents of a given folder to a AWS bucket

To work it needs boto3, and a credentials file with the following format:

aws_access_key_id

aws_secret_access_key

aws_session_token

Basically one token or key per line.

The script can be used with the following command:

python backuper.py -credfile=creditx.txt -folder=./data -bucket=aws-uh-bckup -time=1 -versioning=false 

The arguments are as follows:

-credfile: the File with the AWS credentials (str)

-folder: The folder to be updated to AWS ( str)

-time: the time in minutes between eachupdate ( int) 

-versioning: Use this option to activate Bucker versioning.
