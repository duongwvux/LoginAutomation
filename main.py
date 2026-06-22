from adapters.webhook_app import create_app
from wiring import build_use_case

app = create_app(build_use_case())

if __name__ == "__main__":
    app.run(port=5000)