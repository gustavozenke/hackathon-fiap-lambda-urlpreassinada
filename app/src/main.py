import json
import logging
import os
from datetime import datetime

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from formato_video import FormatoVideo

config = Config(signature_version='s3v4')

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def lambda_handler(event: dict, context):
    try:
        logger.info(f"Mensagem recebida={event}")

        content_type = event['headers'].get('Content-Type', None)
        nome_video = event['headers'].get('Nome-Video', None)
        nome_usuario = event['requestContext']['authorizer']['claims']['username']

        if content_type is None:
            logger.error("Header Content-Type faltando")
            return response(400, {'error': 'Header Content-Type faltando'}, None)

        if nome_video is None:
            logger.error("Header Nome-Video faltando")
            return response(400, {'error': 'Header Nome-Video faltando'}, None)

        if FormatoVideo.from_mime(content_type) is None:
            logger.error("Header Header Content-Type com valor nao permitido faltando")
            return response(400, {'error': 'Header Content-Type com valor nao permitido'}, None)

        s3_client = boto3.client('s3', config=config)
        s3_key = get_object_key(nome_usuario, nome_video, FormatoVideo.from_mime(content_type))
        bucket_name = os.getenv("BUCKET_NAME")

        logger.info(f"Gerando URL pre assinada para upload do video {nome_video}")

        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': s3_key,
                "ServerSideEncryption": "AES256",
                "ContentType": content_type
            },
            ExpiresIn=3600
        )

        body = {'presigned_url': presigned_url}
        headers = {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}

        logger.info(body)
        return response(200, body, headers)

    except KeyError as e:
        logger.error(f'Campo obrigatório faltando: {str(e)}')
        return response(400, {'error': f'Campo obrigatório faltando: {str(e)}'}, None)

    except ClientError as e:
        logger.error(f'Erro ao gerar URL pre assinada no S3: {str(e)}')
        return response(500, {'error': f'Erro ao gerar URL pre assinada no S3: {str(e)}'}, None)

    except Exception as e:
        logger.error(f'Erro generico: {str(e)}')
        return response(500, {'error': f'Erro generico: {str(e)}'}, None)


def get_object_key(nome_usuario, nome_video, formato):
    date_time = datetime.now().strftime("%Y%m%d%H%M%S")
    return "{}-{}-{}.{}".format(nome_usuario, nome_video, date_time, formato)


def response(status_code, body, headers):
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(body)
    }
