import asyncio
import os
from datetime import datetime

from flask import Flask, request, redirect, url_for, render_template
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

from .coreutils import (
    log,
    send_request,
    get_current_user,
    format_map_name,
    CURRENT_FILE_DIRECTORY,
    TEMPLATES_DIRECTORY,
)
from .messages import Messages

# Initialise messages
message = Messages()

# Create the Flask application
app = Flask("Orbis Unum: Web Instance", template_folder=TEMPLATES_DIRECTORY)

# List to store location data
location_data = []


@app.route("/index", methods=["GET", "POST"])
def input_coordinates():
    """
    The route for inputting coordinates in the web variant of Orbis.
    It either renders a form for inputting coordinates or processes
    the coordinates that have been inputted.

    :return: Renders the form for a GET request or redirects to the map view for a POST request.
    """
    error = None
    if request.method == "POST":
        try:
            # Get the string of coordinates from the form
            coordinates_input = request.form.get("coordinates")

            # Split the string into a list of tuples, where each tuple is a pair of coordinates
            coordinates_list = [
                tuple(map(float, coordinates.split(",")))
                for coordinates in coordinates_input.split("\n")
            ]

            # Get the location data for each pair of coordinates
            # and create a list of dictionaries where each dictionary has a 'location'
            # key (with the location data) and an 'ip_address' key (with a None value as IP address is not available)
            location_data[:] = [
                {
                    "location": asyncio.run(get_reverse_geolocation_data(coordinates)),
                    "ip_address": None,
                }
                for coordinates in coordinates_list
            ]

            # Redirect to the map view
            return redirect(url_for("map_view"))

        except Exception as e:
            # Create an error message
            error = Markup(
                message.an_error_occurred(error=str(e))
            )  # mark the error as safe
            log.error(message.an_error_occurred(error=str(e)))

    # Render the input form for a GET request
    return render_template(
        "index.html",
        current_user=get_current_user(),
        current_year=datetime.now().year,
        error=error,
    )


@app.route("/map")
def map_view(map_name: str = "Orbis Web"):
    """
    The route for displaying the map in the web variant of Orbis. It uses the map.html template.
    """
    return render_template(
        "map.html",
        map_data=location_data,
        current_user=get_current_user(),
        map_name=map_name,
    )


def process_user_input(user_input: str) -> list:
    """
    Processes input from user to determine the type, and how to return the results.

    :param user_input: IP; could be a single IP or a text file containing IP Addresses.
    :return: A list containing an IP Address/Addresses.
    """
    if os.path.isfile(user_input):
        with open(user_input, "r") as file:
            log.info(message.loaded_addresses(filename=file.name))
            ip_addresses = [ip.strip() for ip in file.readlines()]
            return ip_addresses
    else:
        return [user_input]


async def get_reverse_geolocation_data(coordinates: tuple) -> dict:
    """
    Gets location data from the given coordinates.

    :param coordinates: A tuple containing the longitude and latitude parts of the coordinates.
    :return: A dictionary of the coordinates' location data.
    """
    log.info(
        message.requesting_data(
            request_type="reverse-geolocation",
            target_title="coordinates",
            target=coordinates,
        )
    )
    coordinates_location_data = await send_request(
        f"https://nominatim.openstreetmap.org/reverse?lat={coordinates[0]}&"
        f"lon={coordinates[1]}&format=json&addressdetails=1"
    )

    return coordinates_location_data


async def get_geolocation_data(ip_address: str) -> tuple:
    """
    Gets geolocation data from the given ip address.

    :param ip_address: Target IP Address.
    :return: A tuple containing ip address, latitude and longitude.
    """

    log.info(
        message.requesting_data(
            request_type="geolocation", target_title="IP", target=ip_address
        )
    )
    ip_coordinates = await send_request(f"http://ip-api.com/json/{ip_address}")
    return (
        ip_coordinates.get("query"),
        ip_coordinates.get("lat"),
        ip_coordinates.get("lon"),
    )


async def get_location_data_list(ip_address: str) -> list:
    """
    Given an IP address, this function returns a list of location data, the IP address itself, and the corresponding
    first coordinate for each IP address.

    :param ip_address: A string containing one or more IP addresses (in a file).
    :return: A list of dictionaries where each dictionary contains the
     location data of an IP address and the IP address itself.
    """
    data_list = []
    ip_addresses = process_user_input(user_input=ip_address)
    coordinates_list = [await get_geolocation_data(ip) for ip in ip_addresses]

    for coordinates in coordinates_list:
        data = {
            "location": await get_reverse_geolocation_data(
                (coordinates[1], coordinates[2])
            ),
            "ip_address": coordinates[0],
        }
        data_list.append(data)

    return data_list


def create_map(map_data: list, map_name: str) -> str:
    """
    Uses the map template to create a new map with the geolocation data returned from the get_location_data function.

    :param map_data: List of dictionaries containing the location data of each IP Address and the IP itself.
    :param map_name: Output filename of the generated map.
    :return: An interactive map in default browser
    (with pins pointing on the areas that correspond the IPs coordinates).
    """
    home_directory = os.path.expanduser("~")
    maps_directory = os.path.join(home_directory, "orbis-maps")

    env = Environment(
        loader=FileSystemLoader(os.path.join(CURRENT_FILE_DIRECTORY, "templates"))
    )

    map_template = env.get_template("map.html")

    rendered_map = map_template.render(
        current_user=get_current_user(),
        current_datetime=datetime.now(),
        map_name=map_name,
        map_data=map_data,
    )

    with open(
        os.path.join(maps_directory, f"{format_map_name(map_name)}.html"),
        "w",
        encoding="utf-8",
    ) as created_map:
        created_map.write(rendered_map)

    return created_map.name
