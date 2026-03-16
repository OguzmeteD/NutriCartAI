import boto3
from boto3.dynamodb.conditions import Key

from app.core.config import settings

_dynamodb = boto3.resource("dynamodb", region_name=settings.aws_default_region)
users_table = _dynamodb.Table(settings.dynamodb_table_users)


def get_user_by_email(email: str) -> dict | None:
    result = users_table.query(
        IndexName="email-index",
        KeyConditionExpression=Key("email").eq(email),
    )
    items = result.get("Items", [])
    return items[0] if items else None


def get_user_by_verification_token(token: str) -> dict | None:
    result = users_table.query(
        IndexName="verification_token-index",
        KeyConditionExpression=Key("verification_token").eq(token),
    )
    items = result.get("Items", [])
    return items[0] if items else None


def get_user_by_id(user_id: str) -> dict | None:
    result = users_table.get_item(Key={"user_id": user_id})
    return result.get("Item")


def put_user(item: dict) -> None:
    users_table.put_item(Item=item)


def update_user(user_id: str, update_expression: str, expression_values: dict, expression_names: dict | None = None) -> None:
    kwargs = {
        "Key": {"user_id": user_id},
        "UpdateExpression": update_expression,
        "ExpressionAttributeValues": expression_values,
    }
    if expression_names:
        kwargs["ExpressionAttributeNames"] = expression_names
    users_table.update_item(**kwargs)
