# Configure backend - terraform.tfstate
terraform {
  backend "s3" {
    bucket = "tech-challenge-terraform-tfstate-serverless"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}