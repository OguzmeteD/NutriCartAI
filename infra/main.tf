terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "nutricarta-tfstate"
    key            = "nutricarta/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "nutricarta-tf-lock"
    encrypt        = true
  }
}

provider "aws" {
  region = var.region
}

module "dynamodb" {
  source = "./modules/dynamodb"

  tables = [
    {
      name          = "nutricarta-users"
      partition_key = "user_id"
      sort_key      = null
      gsi = [
        { name = "email-index",               partition_key = "email" },
        { name = "verification_token-index",  partition_key = "verification_token" },
      ]
    },
    {
      name          = "nutricarta-products"
      partition_key = "product_id"
      sort_key      = null
    },
    {
      name          = "nutricarta-carts"
      partition_key = "user_id"
      sort_key      = "cart_id"
    },
  ]
}

module "s3" {
  source = "./modules/s3"

  project    = var.project
  account_id = var.aws_account_id
  buckets = [
    "product-images",
    "user-uploads",
    "ml-artifacts",
    "app-logs",
  ]
}
