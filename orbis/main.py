import webbrowser

from .coreutils import args, log, path_finder
from .orbis import message, app, create_map, get_location_data_list


def orbis() -> str:
    """
    Returns the usage of both orbis-cli and orbis-web.
    """
    return """
    orbis-cli/orbis-web

    CLI
    ===
       Use 'orbis-cli' command to start the command-line interface variant of Orbis Unum. 
       In CLI mode, you should provide an IP Address or a file containing IP Addresses as an argument. 
       Orbis will fetch the geolocation information for the given IP Address(es) and display it on a map.


    Example
    -------
    orbis-cli --ip 8.8.8.8/orbis-cli ips.txt



    WEB
    ===
       Use 'orbis-web' command to start the web variant of Orbis Unum.
       In WEB mode, you will be presented with a 
       form where you can input geographical coordinates (latitude and longitude).
       After submitting the form, Orbis will fetch the geolocation information for the 
       given coordinates and display it on a map.


    Example
    -------
    orbis-web

    Note: The web interface will be accessible at 'http://localhost:5000/index' after you run the 'orbis-web' command.
    """


def cli():
    """
    The CLI variant of Orbis Unum.
    """
    if args.ip is not None:
        # Create the directory where generated maps will be stored.
        path_finder(["orbis-maps"])
        
        created_map = create_map(
            map_data=get_location_data_list(ip_address=args.ip), map_name=args.output
        )
        
        log.info(message.opening_map(created_map))
        webbrowser.open(created_map)
    else:
        log.info("use orbis-cli -h/--help to show usage.")


def web():
    """
    The web variant of Orbis.
    """
    # Start the Flask app
    log.info("Starting Flask app at http://localhost:5000/index")
    app.run(debug=args.debug)
