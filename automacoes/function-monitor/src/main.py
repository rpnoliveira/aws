import json
import logging
import boto3
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cloudwatch = boto3.client('cloudwatch')
namespace = 'Custom-Lambda-automation-function-monitor'

def convert_utc_to_gmt_minus_3(utc_time):
    utc_dt = datetime.strptime(utc_time, '%Y-%m-%dT%H:%M:%SZ')
    gmt_minus_3_offset = timedelta(hours=-3)
    gmt_minus_3_dt = utc_dt + gmt_minus_3_offset
    
    return gmt_minus_3_dt.strftime('%d-%m-%Y %H:%M:%S')

def lambda_handler(event, context):
    logger.info(json.dumps(event))
    if event.get('detail', {}).get('eventName') == 'UpdateFunctionCode20150331v2':
        event_time_utc = event['detail'].get('eventTime', 'N/A')
        gmt_minus_3_time = convert_utc_to_gmt_minus_3(event_time_utc)
        
        account_id = event['detail']['userIdentity'].get('accountId', 'N/A')
        user_name = event['detail']['userIdentity']['sessionContext']['sessionIssuer'].get('userName', 'N/A')
        function_name = event['detail']['responseElements'].get('functionName')
        
        if not function_name:
            return None

        log_message = (
            "\nUpdate Function Code:\n"
            f"accountId: {account_id}\n"
            f"userName: {user_name}\n"
            f"eventTime: {gmt_minus_3_time}\n"
            f"functionName: {function_name}\n"
        )
        logger.info(log_message)

        metric_data = [
            {
                'MetricName': 'UpdateFunctionCode',
                'Dimensions': [
                    {
                        'Name': 'AccountId',
                        'Value': account_id
                    },
                    {
                        'Name': 'UserName',
                        'Value': user_name
                    },
                    {
                        'Name': 'EventTime',
                        'Value': gmt_minus_3_time
                    },
                    {
                        'Name': 'FunctionName',
                        'Value': function_name
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