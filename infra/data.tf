data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "../${path.module}/src"
  output_path = "../${path.module}/lambda.zip"
}

data "aws_api_gateway_rest_api" "apigateway_rest_api" {
  name = "Pos Tech Hackathon - API Gateway"
}