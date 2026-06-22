from domain.entities import Ticket


class ConsoleNotificationAdapter:
    def send_email(self, ticket: Ticket, message: str) -> None:
        print(f"\n--- [DEMO EMAIL] Gửi tới {ticket.requester_email} ---")
        print(message)
        print("--- hết email ---\n", flush=True)