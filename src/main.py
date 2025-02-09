import json
import logging
import os
from datetime import datetime

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from formato_video import FormatoVideo

config = Config(signature_version='s3v4')

logging.basicConfig(level=logging.INFO)
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


if __name__ == '__main__':
    event = {
        'resource': '/presigned-url',
        'path': '/presigned-url', 'httpMethod': 'GET',
        'headers': {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Authorization': 'Bearer token',
            'Cache-Control': 'no-cache',
            'Host': 'r4789v85wb.execute-api.us-east-1.amazonaws.com',
            'Postman-Token': '7e3b1ace-73d1-48b9-bb54-ff955bcf9e4a',
            'User-Agent': 'PostmanRuntime/7.26.8',
            'X-Amzn-Trace-Id': 'Root=1-679db0c2-5896b31b751dcdf05c4717cf',
            'X-Forwarded-For': '187.10.135.221',
            'X-Forwarded-Port': '443',
            'X-Forwarded-Proto': 'https',
            'Content-Type': 'video/mp4',
            'Nome-Video': "videoteste"
        },
        'multiValueHeaders': {
            'Accept': ['*/*'],
            'Accept-Encoding': ['gzip, deflate, br'],
            'Authorization': [
                'Bearer token'],
            'Cache-Control': ['no-cache'], 'Host': ['r4789v85wb.execute-api.us-east-1.amazonaws.com'],
            'Postman-Token': ['7e3b1ace-73d1-48b9-bb54-ff955bcf9e4a'],
            'User-Agent': ['PostmanRuntime/7.26.8'],
            'X-Amzn-Trace-Id': ['Root=1-679db0c2-5896b31b751dcdf05c4717cf'],
            'X-Forwarded-For': ['187.10.135.221'], 'X-Forwarded-Port': ['443'],
            'X-Forwarded-Proto': ['https']
        },
        'queryStringParameters': None,
        'multiValueQueryStringParameters': None,
        'pathParameters': None,
        'stageVariables': None,
        'requestContext': {
            'resourceId': 'k39o9h',
            'authorizer': {
                'claims': {
                    'origin_jti': '6cde5b5e-2261-431c-932b-e43cd5a9ab2d',
                    'sub': 'd43844c8-1041-7089-4b9d-6b33b2e93cc8', 'token_use': 'access',
                    'scope': 'openid profile email', 'auth_time': '1738387405',
                    'iss': 'https://cognito-idp.us-east-1.amazonaws.com/us-east-1_J7PkosrN7',
                    'exp': 'Sat Feb 01 06:23:25 UTC 2025', 'version': '2', 'iat': 'Sat Feb 01 05:23:25 UTC 2025',
                    'client_id': '4skq4i9bu09lib9o7g46p7g5nd', 'jti': '045815bc-bde9-4a99-a175-9878def59f3a',
                    'username': 'gustavozenke'
                }
            },
            'resourcePath': '/presigned-url', 'httpMethod': 'GET',
            'extendedRequestId': 'FSiOdEcmIAMEjPA=', 'requestTime': '01/Feb/2025:05:27:30 +0000',
            'path': '/prod/presigned-url', 'accountId': '369780787289', 'protocol': 'HTTP/1.1',
            'stage': 'prod', 'domainPrefix': 'r4789v85wb', 'requestTimeEpoch': 1738387650596,
            'requestId': '51a992d6-a72d-461e-b43b-027eda35af0a',
            'identity': {
                'cognitoIdentityPoolId': None,
                'accountId': None,
                'cognitoIdentityId': None,
                'caller': None,
                'sourceIp': '187.10.135.221',
                'principalOrgId': None,
                'accessKey': None,
                'cognitoAuthenticationType': None,
                'cognitoAuthenticationProvider': None, 'userArn': None,
                'userAgent': 'PostmanRuntime/7.26.8', 'user': None
            },
            'domainName': 'r4789v85wb.execute-api.us-east-1.amazonaws.com',
            'deploymentId': '3mchst',
            'apiId': 'r4789v85wb'
        },
        'body': None,
        'isBase64Encoded': False
    }
    lambda_handler(event, None)
