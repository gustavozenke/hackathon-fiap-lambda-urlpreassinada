def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "Hello World!"
    }


if __name__ == '__main__':
    lambda_handler(None, None)
