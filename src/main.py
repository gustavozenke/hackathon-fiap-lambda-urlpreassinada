import boto3
import json
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    try:
        s3_client = boto3.client('s3')

        claims = event['requestContext']['authorizer']['claims']

        metadata = {f'x-amz-meta-{key.replace(":", "_").lower()}': str(value)
                    for key, value in claims.items()}

        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': 'bucket-hackathon-fiap-raw-videos',
                'Key': 'uploads/${filename}',
                'Metadata': metadata
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
