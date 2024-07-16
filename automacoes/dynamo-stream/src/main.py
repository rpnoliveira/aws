import boto3
import json
import logging
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cloudwatch = boto3.client('cloudwatch')
namespace = 'Custom-Lambda-automation-tabela-dynamo'

def converter_para_gmt_minus_3(end_tm):
    if end_tm:
        end_tm = end_tm.replace('Z', '')
        partes = end_tm.split('.')
        data_hora = partes[0]
        end_tm_formatado = data_hora
        formato = '%Y-%m-%dT%H:%M:%S'
        dt_object = datetime.strptime(end_tm_formatado, formato)
        gmt3_offset = timedelta(hours=-3)
        dt_object_gmt3 = dt_object + gmt3_offset
        resultado_formatado = dt_object_gmt3.strftime('%d-%m-%Y %H:%M:%S')
        return resultado_formatado
    else:
        return "Data e hora não disponíveis"

def lambda_handler(event, context):
    logger.info("Evento recebido: %s", json.dumps(event))
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('tabela-dynamo')

    batch_records = []
    for record in event['Records']:
        if record['eventName'] == 'MODIFY':
            new_item = record['dynamodb']['NewImage']
            batch_records.append(new_item)

    if batch_records:
        process_batch(batch_records)

def process_batch(batch_records):
    metric_data = []
    log_messages = []

    for item in batch_records:
        error_log = item.get('error_log', {}).get('S', '')
        source_path = item.get('source_path', {}).get('S', '')
        target_object = item.get('target_object', {}).get('S', '')
        status = item.get('status', {}).get('S', '')
        target_bucket = item.get('target_bucket', {}).get('S', '')
        target_event_name = item.get('target_event_name', {}).get('S', '')
        end_tm = item.get('end_tm', {}).get('S', '')
        
        end_tm_gmt_minus_3 = converter_para_gmt_minus_3(end_tm)
        
        log_message = (
            "\nDados inseridos na tabela:\n"
            f"Registro de erro: {error_log}\n"
            f"Caminho de origem: {source_path}\n"
            f"Objeto alvo: {target_object}\n"
            f"Status: {status}\n"
            f"Bucket Alvo: {target_bucket}\n"
            f"Nome do Evento Alvo: {target_event_name}\n"
            f"Data e hora em GMT-3 formatada: {end_tm_gmt_minus_3}\n"
        )
        log_messages.append(log_message)

        dimensions = [
            {'Name': 'Status', 'Value': status},
            {'Name': 'TargetBucket', 'Value': target_bucket},
            {'Name': 'TargetEventName', 'Value': target_event_name},
        ]

        metric_data.append({
            'MetricName': 'PismoFileCount',
            'Dimensions': dimensions,
            'Value': 1,
            'Unit': 'Count',
        })

    try:
        cloudwatch.put_metric_data(Namespace=namespace, MetricData=metric_data)
        logger.info("Métricas adicionadas com sucesso")
        for log_message in log_messages:
            logger.info(log_message)
    except Exception as e:
        error_message = "Erro ao adicionar métricas: {}".format(str(e))
        logger.error(error_message)