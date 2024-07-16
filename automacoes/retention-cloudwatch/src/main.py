import boto3
import logging


response = boto3.client('logs', region_name='sa-east-1')
paginator = response.get_paginator('describe_log_groups')

def lambda_handler(event, context):

    logGroupList = []
    
    for page in paginator.paginate():
      for logGroup in page["logGroups"]:
            
        if 'retentionInDays' not in logGroup:
                
          logGroupName = logGroup["logGroupName"]
          
          response.put_retention_policy(
              logGroupName=logGroupName,
              retentionInDays=14
          )
          
          logGroupList.append(logGroupName)

    logging.warning(f"List of log groups with retention changed to 14 days > {logGroupList}")