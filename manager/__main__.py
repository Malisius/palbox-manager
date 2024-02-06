# Palbox Manager Copyright Peter Oertel (github@Malisius) 2024
# Released to the public under CC BY-NC (https://creativecommons.org/licenses/by-nc/4.0/)

import json
from flask_app.webapp import app
import sys
from pathlib import Path

CONFIG_FILEPATH: str = "config/palbox_config.json"


def main(args=None):
    # Open config file, creating one if it doesn't exist for some reason
    try:
        Path("config").mkdir(exist_ok=True)
        app.logger.debug("Reading config json file")
        config = {}
        with open(CONFIG_FILEPATH, "r") as f:
            config = json.load(f)
    except FileNotFoundError as e:
        app.logger.warning(
            "Palbox configuration file not found, creating one now"
        )
        with open(CONFIG_FILEPATH, "w") as f:
            json.dump(config, f)
    app.logger.info(config)
    app.run(debug=True)


if __name__ == "__main__":
    sys.exit(main())
