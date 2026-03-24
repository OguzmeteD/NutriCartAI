variable "buckets" {
  description = "List of bucket name suffixes"
  type        = list(string)
}

variable "account_id" {
  description = "AWS account ID used to create globally-unique bucket names"
  type        = string
}

variable "project" {
  description = "Project name prefix for bucket names"
  type        = string
}
