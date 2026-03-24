variable "tables" {
  description = "List of DynamoDB table configurations"
  type = list(object({
    name           = string
    partition_key  = string
    sort_key       = optional(string)
    gsi            = optional(list(object({
      name          = string
      partition_key = string
    })), [])
  }))
}
