import argparse
import getpass
import logging
import os
import subprocess
from datetime import datetime
from typing import Optional, Union

import aiohttp
from rich import print
from rich.logging import RichHandler
from rich.markdown import Markdown
from rich_argparse import RichHelpFormatter

from . import __description__, __epilog__, __version__


async def send_request(endpoint: str) -> Optional[Union[dict, list, None]]:
    """
    Asynchronously sends a GET request to a specified API endpoint and returns the JSON data from it.

    :param endpoint: The API endpoint to send the request to.
    :return: Returns JSON data as a dictionary or list. Returns None if fetching fails.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    error_message = await response.json()
                    log.error(f"An api error occurred: {error_message}")
    except aiohttp.ClientError as error:
        log.error(f"An http error occurred: {error}")
    except Exception as error:
        log.critical(f"An unknown error occurred: {error}")


async def check_updates():
    """
    Checks for latest updates by retrieving the release tag from the releases page of the program from GitHub
    Then compares the remote version tag with the tag in the program.
    If they match, program assumes it's up-to-date.
    If not, print a message notifying the user about the remote version (which is treated as the official new release)
    , and lastly prints the release notes of the presumed new release.
    """
    release_data = await send_request(
        "https://api.github.com/repos/rly0nheart/orbis-unum/releases/latest"
    )
    if release_data.get("tag_name"):
        remote_version = release_data.get("tag_name")
        if remote_version != __version__:
            markdown_release_notes = Markdown(release_data.get("body"))
            log.info(
                f"Orbis Unum {remote_version} (from {__version__}) is available. "
                f"To update, run [italic][green]pip install --upgrade orbis-unum[/][/]"
            )
            print(markdown_release_notes)


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
        description=Markdown(__description__, style="argparse.text"),
        epilog=Markdown(__epilog__, style="argparse.text"),
        formatter_class=RichHelpFormatter,
    )
    parser.add_argument("-i", "--ip", help="ip address or file containing ip addresses")
    parser.add_argument(
        "-o", "--output", help="map output name (default %(default)s)", default="orbis"
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="run orbis-cli in debug mode (also applies to orbis-web)",
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
