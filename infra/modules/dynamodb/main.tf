locals {
  tables_map = { for t in var.tables : t.name => t }
}

resource "aws_dynamodb_table" "this" {
  for_each = local.tables_map

  name         = each.key
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = each.value.partition_key
  range_key    = each.value.sort_key

  attribute {
    name = each.value.partition_key
    type = "S"
  }

  dynamic "attribute" {
    for_each = each.value.sort_key != null ? [each.value.sort_key] : []
    content {
      name = attribute.value
      type = "S"
    }
  }

  dynamic "attribute" {
    for_each = { for gsi in coalesce(each.value.gsi, []) : gsi.partition_key => gsi if gsi.partition_key != each.value.partition_key && gsi.partition_key != each.value.sort_key }
    content {
      name = attribute.key
      type = "S"
    }
  }

  dynamic "global_secondary_index" {
    for_each = { for gsi in coalesce(each.value.gsi, []) : gsi.name => gsi }
    content {
      name            = global_secondary_index.value.name
      hash_key        = global_secondary_index.value.partition_key
      projection_type = "ALL"
    }
  }

  server_side_encryption {
    enabled = true
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Project = "nutricarta"
    Table   = each.key
  }
}
