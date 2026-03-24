output "table_names" {
  description = "Map of logical name → DynamoDB table name"
  value       = { for k, v in aws_dynamodb_table.this : k => v.name }
}

output "table_arns" {
  description = "Map of logical name → DynamoDB table ARN"
  value       = { for k, v in aws_dynamodb_table.this : k => v.arn }
}
