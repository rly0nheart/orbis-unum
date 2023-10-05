**Orbis Unum** is a cross-platform geolocation tool that transforms raw *IP addresses* and *geographical coordinates* into interactive visualizations on a map. With its intuitive interface, users can effortlessly navigate whether they're operating from the command line or using its web-based instance.

## 🔍 What Does Orbis Unum Offer?
### Command Line Interface
- [x] Accepts either a standalone IP or a file loaded with multiple IP addresses.
- [x] Generates an interactive OpenStreetMap with pinpoint accuracy for each IP's location.
#### On selecting any pin, you uncover:
 - [x] Vital IP metadata.
 - [x] Seamless links to:

    * Google Earth for a top-down view or the location.
    * Google Maps Street View for a closer look at the surroundings of the location.
    * Google Image Search to view images of the location and its surroundings.

### Web Interface:
- [x] Accepts individual or bulk pairs of coordinates.
- [x] Mirrors the CLI's functionality, providing an immersive mapping experience.

# Installation
**Orbis Unum** can be installed from PyPI with the following command
```
pip install orbis-unum
```

# Usage
Run thefollowing command to see example usages of the program
```
orbis
```

The output will look like the following
```
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
```
***
![me](https://github.com/rly0nheart/orbis-unum/assets/74001397/1b732a1a-ca46-4d1c-b9af-3d6c744cd366)

