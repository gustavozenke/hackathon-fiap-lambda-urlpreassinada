import json
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.main import lambda_handler


class TestLambdaHandler(unittest.TestCase):

    @patch.dict(os.environ, {"BUCKET_NAME": "bucket-teste-unitario"})
    @patch("boto3.client")
    def test_lambda_handler_sucesso(self, mock_boto3_client):
        mock_s3_client = MagicMock()
        mock_boto3_client.return_value = mock_s3_client
        mock_s3_client.generate_presigned_url.return_value = "https://teste.com/presigned-url"

        event = {
            "headers": {
                "Content-Type": "video/mp4",
                "Nome-Video": "teste.mp4"
            },
            "requestContext": {
                "authorizer": {
                    "claims": {"username": "testuser"}
                }
            }
        }

        response_data = lambda_handler(event, None)
        self.assertEqual(response_data["statusCode"], 200)
        self.assertIn("presigned_url", json.loads(response_data["body"]))

    def test_lambda_handler_faltando_content_type(self):
        event = {
            "headers": {
                "Nome-Video": "teste.mp4"
            },
            "requestContext": {
                "authorizer": {
                    "claims": {"username": "testuser"}
                }
            }
        }

        response_data = lambda_handler(event, None)
        self.assertEqual(response_data["statusCode"], 400)
        self.assertIn("Header Content-Type faltando", response_data["body"])

    def test_lambda_handler_faltando_nome_video(self):
        event = {
            "headers": {
                "Content-Type": "video/mp4"
            },
            "requestContext": {
                "authorizer": {
                    "claims": {"username": "testuser"}
                }
            }
        }

        response_data = lambda_handler(event, None)
        self.assertEqual(response_data["statusCode"], 400)
        self.assertIn("Header Nome-Video faltando", response_data["body"])

    @patch("boto3.client")
    def test_lambda_erro(self, mock_boto3_client):
        mock_s3_client = MagicMock()
        mock_boto3_client.return_value = mock_s3_client
        mock_s3_client.generate_presigned_url.side_effect = Exception("S3 Error")

        event = {
            "headers": {
                "Content-Type": "video/mp4",
                "Nome-Video": "teste.mp4"
            },
            "requestContext": {
                "authorizer": {
                    "claims": {"username": "testuser"}
                }
            }
        }

        response_data = lambda_handler(event, None)
        self.assertEqual(response_data["statusCode"], 500)
        self.assertIn("Erro generico", response_data["body"])
