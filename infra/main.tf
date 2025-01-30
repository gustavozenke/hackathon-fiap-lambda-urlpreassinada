terraform {
  backend "s3" {
    bucket = "hackathon-fiap-terraform-tfstate"
    key    = "lambda-urlpreassinada.tfstate"
    region = "us-east-1"
  }
}