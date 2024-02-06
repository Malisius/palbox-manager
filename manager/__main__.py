# Palbox Manager Copyright Peter Oertel (github@Malisius) 2024
# Released to the public under CC BY-NC (https://creativecommons.org/licenses/by-nc/4.0/)

import json
import sys
from pathlib import Path
from flask import Flask, render_template, request, session, redirect, url_for
from logging.config import dictConfig
from functools import wraps

CONFIG_FILEPATH: str = "config/palbox_config.json"
config = {}


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


def check_allowed(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not config.get("manager"):
            app.logger.info(
                "Didn't find correct manager configuration, redirecting to first setup."
            )
            return redirect(url_for("setup"))

        if not session.get("signedin"):
            return redirect(url_for("signin"))

        return func(*args, **kwargs)

    return inner


@app.route("/")
@check_allowed
def home() -> str:
    return render_template("dashboard.html", location="dashboard")


@app.route("/signin", methods=["GET", "POST"])
@check_allowed
def signin() -> str:
    if request.method == "GET":
        return render_template("signin.html")


@app.route("/stats")
@check_allowed
def stats() -> str:
    return render_template("stats.html", location="stats")


@check_allowed
@app.route("/setup")
def setup() -> str:
    return render_template("setup.html", location="setup")


def main(args=None):
    # Open config file, creating one if it doesn't exist for some reason
    try:
        Path("config").mkdir(exist_ok=True)
        app.logger.debug("Reading config json file")
        with open(CONFIG_FILEPATH, "r") as f:
            config = json.load(f)
    except FileNotFoundError as e:
        app.logger.warning(
            "Palbox configuration file not found, creating one now"
        )
        with open(CONFIG_FILEPATH, "w") as f:
            json.dump(config, f)
    app.logger.debug(config)
    app.run(debug=True)


if __name__ == "__main__":
    sys.exit(main())
