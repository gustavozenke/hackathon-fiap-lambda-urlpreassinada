resource "aws_lambda_function" "this" {
  filename      = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256

  function_name = var.function_name
  role          = var.function_role
  handler       = var.handler
  runtime       = var.runtime
  timeout       = var.timeout

  environment {
    variables = {
      BUCKET_NAME = var.bucket_name
      env = "prod"
    }
  }

  layers = [aws_lambda_layer_version.lambda_layer.arn]
}

# Permissão para a função Lambda ser invocada pelo API Gateway
resource "aws_lambda_permission" "allow_api_gateway_presigned_url" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = var.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = data.aws_api_gateway_rest_api.apigateway_rest_api.arn
}