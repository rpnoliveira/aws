import boto3

rds_client = boto3.client('rds')

def lambda_handler(event, context):
    rds_client.stop_db_cluster(
    DBClusterIdentifier='aurora-name-cluster'
    )