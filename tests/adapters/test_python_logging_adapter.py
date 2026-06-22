import unittest

from adapters.python_logging_adapter import PythonLoggingAdapter


class TestPythonLoggingAdapter(unittest.TestCase):
    def test_log_forwards_message_to_python_logging(self):
        adapter = PythonLoggingAdapter()

        with self.assertLogs("login_automation", level="INFO") as captured:
            adapter.log("ticket T-1 processed")

        self.assertIn("ticket T-1 processed", captured.output[0])


if __name__ == "__main__":
    unittest.main()