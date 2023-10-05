import argparse
import getpass
import logging
import os
import subprocess
from datetime import datetime

import requests
from rich import print
from rich.logging import RichHandler
from rich.markdown import Markdown

from . import __version__, __author__, __about__
from .messages import Messages

message = Messages()


def send_request(endpoint) -> dict:
    """
    Sends a GET request to the specified endpoint and returns JSON

    :param endpoint: url endpoint to send request to
    :return: Dictionary response (JSON)
    """
    try:
        with requests.get(endpoint) as response:
            response_data = response.json()
        return response_data
    except KeyboardInterrupt:
        logging.warning("User interruption detected (Ctrl+C).")
    except Exception as error:
        logging.error(message.an_error_occurred(error=str(error)))


def check_updates():
    """
    Checks for latest updates by retrieving the release tag from the releases page of the program from GitHub
    Then compares the remote version tag with the tag in the program.
    If they match, program assumes it's up-to-date.
    If not, print a message notifying the user about the remote version (which is treated as the official new release)
    , and lastly prints the release notes of the presumed new release.
    """
    release_data = send_request(
        "https://api.github.com/repos/rly0nheart/orbis-unum/releases/latest"
    )

    remote_version = release_data.get("tag_name")
    if remote_version != __version__:
        markdown_release_notes = Markdown(release_data.get("body"))
        log.info(f"Orbis Unum {remote_version} is available.\n")
        print(markdown_release_notes)
    else:
        pass


def path_finder(directories: list) -> None:
    """
    Checks if the specified directories exist.
    If not, it creates them.

    :param directories: List of directories to check and create
    :return: None
    """
    # Construct path to the user's home directory
    home_directory = os.path.expanduser("~")

    for directory in directories:
        # Construct and create each directory from the directories list if it doesn't already exist
        os.makedirs(os.path.join(home_directory, directory), exist_ok=True)


def clear_screen():  # -> A cleared screen
    """
    Clear the terminal screen/
    If Operating system is Windows, uses the 'cls' command. Otherwise, uses the 'clear' command

    :return: Uhh, a cleared screen? haha
    """
    subprocess.call("cmd.exe /c cls" if os.name == "nt" else "clear")


def get_current_user() -> str:
    """
    Gets current logged-in user's username.

    :return: Current user's username.
    """
    return getpass.getuser()


def format_map_name(map_name: str) -> str:
    """
    This function takes a string and adds a timestamp to it in a different format depending on the operating system.

    :param map_name: A string to which the timestamp will be appended.
    :return: A string with the timestamp appended.
    """

    # Check the name of the operating system using os.name
    if os.name == "nt":
        # If the operating system is Windows, then use this format for the timestamp
        formatted_map_name = datetime.now().strftime(f"{map_name}_%d-%m-%Y %H-%M-%S%p")
    else:
        # If the operating system is not Windows (e.g., Unix or Linux), then use this format for the timestamp
        formatted_map_name = datetime.now().strftime(f"{map_name}_%d-%m-%Y %H:%M:%S%p")

    # Return the formatted map name
    return formatted_map_name


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=f"Orbis Unum" f" — by {__author__}" f" ({__about__})",
        epilog="🌍 IP Geolocator & Coordinate Mapper 📍",
    )
    parser.add_argument("-i", "--ip", help="ip address or file containing ip addresses")
    parser.add_argument(
        "-o", "--output", help="map output name (default %(default)s)", default="orbis"
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="run orbis-cli in debug mode",
        action="store_true",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    return parser


def set_loglevel(debug_mode: bool) -> logging.getLogger:
    """
    Configure and return a logging object with the specified log level.

    :param debug_mode: If True, the log level is set to "NOTSET". Otherwise, it is set to "INFO".zzz
    :return: A logging object configured with the specified log level.
    """
    logging.basicConfig(
        level="NOTSET" if debug_mode else "INFO",
        format="%(message)s",
        handlers=[
            RichHandler(markup=True, log_time_format="%H:%M:%S", show_level=True)
        ],
    )
    return logging.getLogger("Orbis Unum")


args = create_parser().parse_args()
log = set_loglevel(debug_mode=args.debug)

# Construct the path to the directory containing the current script
CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the templates directory
TEMPLATES_DIRECTORY = os.path.join(CURRENT_FILE_DIRECTORY, "templates")
