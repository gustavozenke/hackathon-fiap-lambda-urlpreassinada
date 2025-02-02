import json
from datetime import datetime

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

config = Config(signature_version='s3v4')


def lambda_handler(event: dict, context):
    try:
        s3_client = boto3.client('s3', config=config)

        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': "bucket-hackathon-fiap-raw-videos",
                'Key': get_object_key(event),
                "ServerSideEncryption": "AES256",
                "ContentType": "video/x-ms-wmv"
            },
            ExpiresIn=3600
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'presigned_url': presigned_url
            })
        }

    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Campo obrigatório faltando: {str(e)}'})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Erro no S3: {str(e)}'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def get_object_key(event: dict):
    username = event['requestContext']['authorizer']['claims']['username']
    date_time = datetime.now().strftime("%Y%m%d%H%M%S")
    return "{}-{}.wmv".format(username, date_time)


if __name__ == '__main__':
    event = {
        'resource': '/presigned-url',
        'path': '/presigned-url', 'httpMethod': 'GET',
        'headers': {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Authorization': 'Bearer eyJraWQiOiJVVmNGaWxVdzFxa29yUUxQT2o4bGMzeEFiR3NxNWp4eTdEUWVJcTYwSkU0PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJkNDM4NDRjOC0xMDQxLTcwODktNGI5ZC02YjMzYjJlOTNjYzgiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9KN1Brb3NyTjciLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiI0c2txNGk5YnUwOWxpYjlvN2c0NnA3ZzVuZCIsIm9yaWdpbl9qdGkiOiI2Y2RlNWI1ZS0yMjYxLTQzMWMtOTMyYi1lNDNjZDVhOWFiMmQiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXV0aF90aW1lIjoxNzM4Mzg3NDA1LCJleHAiOjE3MzgzOTEwMDUsImlhdCI6MTczODM4NzQwNSwianRpIjoiMDQ1ODE1YmMtYmRlOS00YTk5LWExNzUtOTg3OGRlZjU5ZjNhIiwidXNlcm5hbWUiOiJndXN0YXZvemVua2UifQ.T2I3mzzKQwQESaQhY5dte9tQM78N7uFKaLFEc5SYFkApkXupclGcWcK5mE0iijrbwuTiYA2CrzGG11PTzy-NTslgOCOVYSLjaNiS_arHynce2l2DoOSfehLmdrmLl064hycXtjaLyjJw65nqO3hE9agltmoP7mdqQlU-LQrAgn-6lhSYeW2BnNq1pJCC1U9XAuuEnfHBKo_cTydWEefnpKbCMPfeVEZDSfFcKzBpxMTVcd5X5v-82ICYGH7WvrTDG6YlrLVPTPfb5JVQS7o0XT7_f88bmJwnaTTOe_oe0LOBRoNQQKTkFgyk-jRjMKLy4eoWgEa_VMBOz53_pvVO4Q',
            'Cache-Control': 'no-cache', 'Host': 'r4789v85wb.execute-api.us-east-1.amazonaws.com',
            'Postman-Token': '7e3b1ace-73d1-48b9-bb54-ff955bcf9e4a', 'User-Agent': 'PostmanRuntime/7.26.8',
            'X-Amzn-Trace-Id': 'Root=1-679db0c2-5896b31b751dcdf05c4717cf', 'X-Forwarded-For': '187.10.135.221',
            'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'
        },
        'multiValueHeaders': {
            'Accept': ['*/*'],
            'Accept-Encoding': ['gzip, deflate, br'],
            'Authorization': [
                'Bearer eyJraWQiOiJVVmNGaWxVdzFxa29yUUxQT2o4bGMzeEFiR3NxNWp4eTdEUWVJcTYwSkU0PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJkNDM4NDRjOC0xMDQxLTcwODktNGI5ZC02YjMzYjJlOTNjYzgiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9KN1Brb3NyTjciLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiI0c2txNGk5YnUwOWxpYjlvN2c0NnA3ZzVuZCIsIm9yaWdpbl9qdGkiOiI2Y2RlNWI1ZS0yMjYxLTQzMWMtOTMyYi1lNDNjZDVhOWFiMmQiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXV0aF90aW1lIjoxNzM4Mzg3NDA1LCJleHAiOjE3MzgzOTEwMDUsImlhdCI6MTczODM4NzQwNSwianRpIjoiMDQ1ODE1YmMtYmRlOS00YTk5LWExNzUtOTg3OGRlZjU5ZjNhIiwidXNlcm5hbWUiOiJndXN0YXZvemVua2UifQ.T2I3mzzKQwQESaQhY5dte9tQM78N7uFKaLFEc5SYFkApkXupclGcWcK5mE0iijrbwuTiYA2CrzGG11PTzy-NTslgOCOVYSLjaNiS_arHynce2l2DoOSfehLmdrmLl064hycXtjaLyjJw65nqO3hE9agltmoP7mdqQlU-LQrAgn-6lhSYeW2BnNq1pJCC1U9XAuuEnfHBKo_cTydWEefnpKbCMPfeVEZDSfFcKzBpxMTVcd5X5v-82ICYGH7WvrTDG6YlrLVPTPfb5JVQS7o0XT7_f88bmJwnaTTOe_oe0LOBRoNQQKTkFgyk-jRjMKLy4eoWgEa_VMBOz53_pvVO4Q'],
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
