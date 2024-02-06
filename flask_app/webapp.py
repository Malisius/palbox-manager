import sys
from flask import Flask, render_template
from logging.config import dictConfig

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "DEBUG", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)


@app.route("/")
def home() -> str:
    return render_template("dashboard.html", location="dashboard")


@app.route("/stats")
def stats() -> str:
    return render_template("stats.html", location="stats")


@app.route("/setup")
def setup() -> str:
    return render_template("setup.html", location="setup")


if __name__ == "__main__":
    app.logger.critical(
        "This script shouldn't be run directly. Run the manager instead."
    )
    sys.exit()
