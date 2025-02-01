locals {
  layer_path        = "requirements"
  layer_zip_name    = "layer.zip"
  layer_name        = "lambda_layer"
  requirements_name = "requirements.txt"
  requirements_path = "${path.module}/${local.layer_path}/${local.requirements_name}"
}

resource "null_resource" "lambda_layer" {
  triggers = {
    requirements = filesha1(local.requirements_path)
  }
  provisioner "local-exec" {
    command = <<EOT
      cd ${local.layer_path}
      rm -rf python
      mkdir python
      pip3 install -r ${local.requirements_name} -t python/
      zip -r ${local.layer_zip_name} python/
    EOT
  }
}

resource "aws_s3_bucket" "lambda_layer" {
  bucket_prefix = "lambda-layer"
}

resource "aws_s3_object" "lambda_layer_zip" {
  bucket     = aws_s3_bucket.lambda_layer.id
  key        = "lambda_layers/${local.layer_name}/${local.layer_zip_name}"
  source     = "${local.layer_path}/${local.layer_zip_name}"
  depends_on = [null_resource.lambda_layer]
}

resource "aws_lambda_layer_version" "lambda_layer" {
  s3_bucket           = aws_s3_bucket.lambda_layer.id
  s3_key              = aws_s3_object.lambda_layer_zip.key
  layer_name          = local.layer_name
  compatible_runtimes = ["python3.9"]
  skip_destroy        = true
  depends_on          = [aws_s3_object.lambda_layer_zip]
}