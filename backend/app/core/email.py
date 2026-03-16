import boto3
from botocore.exceptions import ClientError

from app.core.config import settings

_ses = boto3.client("ses", region_name=settings.aws_default_region)


def send_verification_email(to_email: str, token: str) -> None:
    verify_url = f"{settings.base_url}/auth/verify-email?token={token}"
    subject = "Verify your NutriCartAI email"
    body_text = f"Click the link to verify your email:\n\n{verify_url}\n\nThis link expires in 24 hours."
    body_html = (
        f"<p>Click the link to verify your email:</p>"
        f'<p><a href="{verify_url}">{verify_url}</a></p>'
        f"<p>This link expires in 24 hours.</p>"
    )

    try:
        _ses.send_email(
            Source=settings.ses_sender_email,
            Destination={"ToAddresses": [to_email]},
            Message={
                "Subject": {"Data": subject},
                "Body": {
                    "Text": {"Data": body_text},
                    "Html": {"Data": body_html},
                },
            },
        )
    except ClientError as exc:
        raise RuntimeError(f"SES send failed: {exc.response['Error']['Message']}") from exc
