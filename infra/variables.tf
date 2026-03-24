variable "project" {
  description = "Project name used as a prefix for all resources"
  type        = string
  default     = "nutricarta"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "aws_account_id" {
  description = "AWS account ID (used for globally-unique S3 bucket names)"
  type        = string
}
