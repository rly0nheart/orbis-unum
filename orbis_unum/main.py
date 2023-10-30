import webbrowser

from .coreutils import args, log, path_finder, check_updates, Markdown, print
from .orbis import message, app, create_map, get_location_data_list


def orbis():
    print(
        Markdown(
            markup="""
# Orbis Unum

## CLI
> Use the `orbis-cli` command to start the command-line interface variant of **Orbis Unum**. 
In CLI mode, you should provide an IP Address or a file containing IP Addresses as an argument. 
Orbis will fetch the geolocation information for the given IP Address(es) and display it on a map.
    
```
orbis-cli --ip 8.8.8.8/orbis-cli ips.txt
```


## WEB
> Use the `orbis-web` command to start the web variant of **Orbis Unum**.
In WEB mode, you will be presented with a form where you can input geographical coordinates 
(latitude and longitude). After submitting the form, Orbis will fetch the geolocation information for the 
given coordinates and display it on a map.
    
```
orbis-web
```
    
### Note
> The web interface will be accessible at http://localhost:5000/index after you run the 'orbis-web' command.
"""
        )
    )


def orbis_cli():
    """
    The CLI variant of Orbis Unum.
    """
    import asyncio

    if args.ip:
        # Create the directory where generated maps will be stored.
        path_finder(["orbis-maps"])

        asyncio.run(check_updates())
        map_data = asyncio.run(get_location_data_list(ip_address=args.ip))
        created_map = create_map(map_data=map_data, map_name=args.output)

        log.info(message.opening_map(created_map))
        webbrowser.open(created_map)
    else:
        log.info("use orbis-cli -h/--help to show usage.")


def orbis_web():
    """
    The web variant of Orbis Unum.
    """
    check_updates()

    # Start the Flask app
    log.info("Hosting Flask app at http://localhost:5000/index")
    app.run(debug=args.debug)
