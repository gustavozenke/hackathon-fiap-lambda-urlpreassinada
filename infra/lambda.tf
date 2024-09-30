data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "../${path.module}/src"
  output_path = "../${path.module}/lambda.zip"
}

resource "aws_lambda_function" "test_lambda" {
  filename      = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256

  function_name = "postech-serverless"
  role          = "arn:aws:iam::975748149223:role/LabRole"
  handler       = "main.lambda_handler"

  runtime = "python3.8"

  environment {
    variables = {
      foo = "bar"
    }
  }
}