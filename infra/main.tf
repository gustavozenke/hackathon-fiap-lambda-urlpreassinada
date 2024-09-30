# Configure backend - terraform.tfstate
terraform {
  backend "s3" {
    bucket = "tech-challenge-terraform-tfstate"
    key    = "terraform-serverless.tfstate"
    region = "us-east-1"
  }
}