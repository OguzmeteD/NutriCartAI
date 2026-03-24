output "bucket_names" {
  description = "Map of logical name → S3 bucket name"
  value       = { for k, v in aws_s3_bucket.this : k => v.bucket }
}

output "bucket_arns" {
  description = "Map of logical name → S3 bucket ARN"
  value       = { for k, v in aws_s3_bucket.this : k => v.arn }
}
