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
usage: gpx-starting-point-extract.py [-h] --output OUTPUTFILE [--bounds] [--category NAME] [--symbol NAME] INPUTFILE [INPUTFILE ...]

positional arguments:
  INPUTFILE            GPX input files

options:
  -h, --help           show this help message and exit
  --output OUTPUTFILE  GPX output file
  --bounds             add metadata with bounds
  --category NAME      POI category (Garmin Extension)
  --symbol NAME        waypoint symbol
```
