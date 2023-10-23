![orbis](https://github.com/rly0nheart/orbis-unum/assets/74001397/628ddd47-f50b-4305-9c67-8535eb53d5d3)

**Orbis Unum** is a cross-platform geolocation tool that transforms raw *IP addresses* and *geographical coordinates* into interactive visualizations on a map. With its intuitive interface, users can effortlessly navigate whether they're operating from the command line or using its web-based instance.

![Python](https://img.shields.io/badge/Python-14354C?style=flat&logo=python) ![html](https://img.shields.io/badge/HTML-orange?style=flat&logo=html5&logoColor=white) ![flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask) [![Upload Python Package](https://github.com/rly0nheart/orbis-unum/actions/workflows/python-publish.yml/badge.svg)](https://github.com/rly0nheart/orbis-unum/actions/workflows/python-publish.yml) [![CodeQL](https://github.com/rly0nheart/orbis-unum/actions/workflows/codeql.yml/badge.svg)](https://github.com/rly0nheart/orbis-unum/actions/workflows/codeql.yml)

## 🔍 What Does Orbis Unum Offer?
### Command Line Interface
- [x] Accepts either a standalone IP or a file loaded with multiple IP addresses.
- [x] Generates an interactive OpenStreetMap with pinpoint accuracy for each IP's location.
#### On selecting any pin, you uncover:
 - [x] Vital IP/Coordinates metadata.
 - [x] Seamless links to:

    * Google Earth for a top-down view or the location.
    * Google Maps Street View for a closer look at the surroundings of the location.
    * Google Image Search to view images of the location and its surroundings.

### Web Interface
- [x] Accepts individual or bulk pairs of coordinates.
- [x] Mirrors the CLI's functionality, providing an immersive mapping experience.

# Installation
**Orbis Unum** can be installed from PyPI with the following command
```
pip install orbis-unum
```

# Usage
Run the following command to see example usages of the program
```
orbis
```

The output should look like the following
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

Run the following command to see the usage of the command-line instance of Orbis Unum
```
orbis-cli --help
```
The output should look like the following
```
usage: orbis-cli [-h] [-i IP] [-o OUTPUT] [-d] [-v]

Orbis Unum — by Richard Mwewa (https://about.me/rly0nheart)

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        ip address or file containing ip addresses
  -o OUTPUT, --output OUTPUT
                        map output name (default orbis)
  -d, --debug           run orbis-cli in debug mode
  -v, --version         show program's version number and exit

🌍 IP Geolocator & Coordinate Mapper 📍 
```
***
![python-powered](https://github.com/rly0nheart/orbis-unum/assets/74001397/c2d2d150-d8e7-4748-bd97-0ca62685fa91)

<a href="https://www.buymeacoffee.com/_rly0nheart"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=_rly0nheart&button_colour=40DCA5&font_colour=ffffff&font_family=Comic&outline_colour=000000&coffee_colour=FFDD00" /></a>

![me](https://github.com/rly0nheart/orbis-unum/assets/74001397/885e8710-8756-43c8-b63e-109b55af2b37)



