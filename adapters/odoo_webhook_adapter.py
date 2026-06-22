from domain.entities import Ticket


class InvalidWebhookPayloadError(Exception):
    """Payload thiếu field bắt buộc (ticket_id, partner_email)."""


def parse_webhook_payload(payload: dict) -> Ticket:
    try:
        ticket_id = payload["ticket_id"]
        requester_email = payload["partner_email"]
    except KeyError as exc:
        raise InvalidWebhookPayloadError(f"Thiếu field bắt buộc: {exc}") from exc

    subject = payload.get("subject", "")
    description = payload.get("description", "")
    content = f"{subject}\n{description}".strip()

    return Ticket(id=ticket_id, content=content, requester_email=requester_email)