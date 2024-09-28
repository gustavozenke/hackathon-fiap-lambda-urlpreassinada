from datetime import datetime, timezone, timedelta


def payload_encode_token(event):
    return {
        "cpf": event.get("cpf"),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10)

    }


def payload_response_gateway(status_code, body):
    return {
        "isBase64Encoded": False,
        "statusCode": status_code,
        "body": body,
        "headers": {
            "content-type": "application/json"
        }
    }


def payload_response_buscar_cliente(status_code, body):
    return {
        "status_code": status_code,
        "body": body
    }
