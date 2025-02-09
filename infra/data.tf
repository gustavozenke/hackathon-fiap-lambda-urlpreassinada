data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "../${path.module}/src"
  output_path = "../${path.module}/lambda.zip"
}