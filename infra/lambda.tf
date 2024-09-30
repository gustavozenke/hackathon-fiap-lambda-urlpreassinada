data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "../${path.module}/src"
  output_path = "../${path.module}/lambda.zip"
}

resource "aws_lambda_function" "this" {
  filename      = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256

  function_name = var.function_name
  role          = var.function_role
  handler       = var.handler
  runtime       = var.runtime

  environment {
    variables = {
      mongodb_uri = "mongodb+srv://tech:qPJ7uBMFNUkRTuP5@cluster0.ilvmgzj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
      database = "TechChallenge",
      algorithm = "HS256",
      secret = "5d319eaf5a5be8e83b0e8777d98baeb783d72f8a"
    }
  }

  layers = [aws_lambda_layer_version.lambda_layer.arn]
}