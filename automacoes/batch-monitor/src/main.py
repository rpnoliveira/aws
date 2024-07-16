import json
import logging
import boto3
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cloudwatch = boto3.client('cloudwatch')
namespace = 'Custom-Lambda-automation-batch-monitor'

def convert_utc_to_gmt_minus_3(utc_time):
    utc_dt = datetime.strptime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
    gmt_minus_3_offset = timedelta(hours=-3)
    gmt_minus_3_dt = utc_dt + gmt_minus_3_offset
    
    return gmt_minus_3_dt.strftime('%d-%m-%Y %H:%M:%S')

def lambda_handler(event, context):
    logger.info(json.dumps(event))
    if event.get('detail-type') == 'Batch Job State Change':
        event_time_utc = event['time']
        gmt_minus_3_time = convert_utc_to_gmt_minus_3(event_time_utc)
        
        account_id = event['account']
        job_definition_full = event['detail']['jobDefinition']

        job_definition_parts = job_definition_full.split('/')
        job_name = job_definition_parts[-1].split(':')[0]
        revision = job_definition_parts[-1].split(':')[1]
        
        job_id = event['detail']['jobId']
        status = event['detail']['status']
        
        log_message = (
            "\nBatch Job State Change:\n"
            f"AccountId: {account_id}\n"
            f"EventTime: {gmt_minus_3_time}\n"
            f"JobName: {job_name}\n"
            f"JobId: {job_id}\n"
            f"Status: {status}\n"
            f"Revision: {revision}\n"
        )
        logger.info(log_message)

        metric_data = [
            {
                'MetricName': 'BatchJobStateChange',
                'Dimensions': [
                    {
                        'Name': 'AccountId',
                        'Value': account_id
                    },
                    {
                        'Name': 'EventTime',
                        'Value': gmt_minus_3_time
                    },
                    {
                        'Name': 'JobName',
                        'Value': job_name
                    },
                    {
                        'Name': 'JobId',
                        'Value': job_id
                    },
                    {
                        'Name': 'Status',
                        'Value': status
                    },
                    {
                        'Name': 'Revision',
                        'Value': revision
                    },
                ],
                'Value': 1,
                'Unit': 'Count'
            }
        ]
        
        try:
            cloudwatch.put_metric_data(Namespace=namespace, MetricData=metric_data)
            logger.info("Métricas adicionadas com sucesso")
        except Exception as e:
            error_message = "Erro ao adicionar métricas: {}".format(str(e))
            logger.error(error_message)