# GPX starting point extract

The script reads from multiple GPX files.
The first waypoint in each of the input files is retrieved and all the waypoints are written to a new GPX file.

## Use Case

The purpose of this script is to create a file with only the relevant data for a car navigation system's route guidance
to navigate to the starting points of hiking tracks.

I am using it to extract the starting points from GPX files provided with hiking guidebooks of [Rother Bergverlag](https://www.rother.de).
The output file works well with my [Garmin Car Navigation](https://www.garmin.com/en-US/c/automotive/car-gps-navigation/) system.

## Usage

```sh
usage: gpx-starting-point-extract.py [-h] --output OUTPUTFILE [--bounds] INPUTFILE [INPUTFILE ...]

positional arguments:
  INPUTFILE            files to write

options:
  -h, --help           show this help message and exit
  --output OUTPUTFILE  file to write
  --bounds             add metadata with bounds
```
