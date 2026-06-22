from flask import Flask, jsonify, request

from domain.process_login_ticket_use_case import ProcessLoginTicketUseCase

from .odoo_webhook_adapter import InvalidWebhookPayloadError, parse_webhook_payload


def create_app(use_case: ProcessLoginTicketUseCase) -> Flask:
    app = Flask(__name__)

    @app.post("/webhooks/odoo/ticket-created")
    def handle_ticket_created():
        try:
            ticket = parse_webhook_payload(request.get_json(force=True) or {})
        except InvalidWebhookPayloadError as exc:
            return jsonify({"error": str(exc)}), 400

        try:
            action = use_case.handle(ticket)
        except Exception as exc:  # noqa: BLE001 - không để lỗi 1 ticket làm sập worker
            app.logger.exception("Lỗi xử lý ticket %s", ticket.id)
            return jsonify({"error": "internal_error", "detail": str(exc)}), 500

        return jsonify({"ticket_id": ticket.id, "action": action.value}), 200

    return app
