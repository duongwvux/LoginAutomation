import logging

logger = logging.getLogger("login_automation")


class PythonLoggingAdapter:
    def log(self, event: str) -> None:
        logger.info(event)