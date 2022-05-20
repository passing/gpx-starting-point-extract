#!/usr/bin/python3

import argparse
import pathlib
import sys
import xml.etree.ElementTree as ET


gpx_attributes = {
    "version": "1.1",
    "creator": "https://github.com/passing/gpx-starting-point-extract",
    "xmlns": "http://www.topografix.com/GPX/1/1",
    "xmlns:gpxx": "http://www.garmin.com/xmlschemas/GpxExtensions/v3",
}
namespaces = {
    "1.0": "http://www.topografix.com/GPX/1/0",
    "1.1": "http://www.topografix.com/GPX/1/1",
}
precision = 9


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files",
        type=str,
        nargs="+",
        metavar="INPUTFILE",
        help="GPX input files",
    )
    parser.add_argument(
        "--output",
        type=str,
        metavar="OUTPUTFILE",
        required=True,
        help="GPX output file",
    )
    parser.add_argument(
        "--bounds",
        action="store_true",
        help="add metadata with bounds",
    )
    parser.add_argument(
        "--category",
        type=str,
        metavar="NAME",
        default=None,
        help="POI category (Garmin Extension)",
    )
    parser.add_argument(
        "--symbol",
        type=str,
        metavar="NAME",
        default=None,
        help="waypoint symbol",
    )
    return parser.parse_args()


def get_gpx_namespace(root):
    version = root.get("version")
    namespace = namespaces[version]

    return {"": namespace}


def get_first_waypoint_from_file(filename):
    # parse file and get root
    root = ET.parse(filename).getroot()

    # get default namespace based on gpx version
    ns = get_gpx_namespace(root)

    # find the first waypoint
    wpt = root.find("wpt", namespaces=ns)
    if wpt is None:
        return None

    # get waypoint properties
    lat = wpt.get("lat")
    lon = wpt.get("lon")
    name = wpt.find("name", namespaces=ns)
    ele = wpt.find("ele", namespaces=ns)

    # get basename without extension from filename
    basename = pathlib.Path(filename).stem

    waypoint = {
        "basename": basename,
        "name": name.text,
        "lat": round(float(lat), precision),
        "lon": round(float(lon), precision),
        "ele": int(float(ele.text)) if ele is not None else None,
    }

    return waypoint


def get_first_waypoints_from_files(filenames):
    waypoints = []

    for filename in filenames:
        waypoint = get_first_waypoint_from_file(filename)
        if waypoint is None:
            print("no waypoint found in {}".format(filename), file=sys.stderr)
        else:
            waypoints.append(waypoint)

    return waypoints


def get_waypoints_bounds(waypoints):
    bounds = {
        "minlat": str(min(wpt["lat"] for wpt in waypoints)),
        "maxlat": str(max(wpt["lat"] for wpt in waypoints)),
        "minlon": str(min(wpt["lon"] for wpt in waypoints)),
        "maxlon": str(max(wpt["lon"] for wpt in waypoints)),
    }

    return bounds


def create_gpx(waypoints, category, symbol):
    # create root element
    gpx = ET.Element("gpx", gpx_attributes)

    # create wpt elements
    for waypoint in waypoints:
        wpt = ET.SubElement(
            gpx,
            "wpt",
            attrib={"lat": str(waypoint["lat"]), "lon": str(waypoint["lon"])},
        )
        ET.SubElement(wpt, "name").text = waypoint["basename"]
        ET.SubElement(wpt, "desc").text = waypoint["name"]

        # add elevation when available
        if waypoint["ele"] is not None:
            ET.SubElement(wpt, "ele").text = str(waypoint["ele"])

        # add symbol when provided
        if symbol is not None:
            ET.SubElement(wpt, "sym").text = symbol

        # add gpxx waypoint extensions
        ext = ET.SubElement(wpt, "extensions")
        wpt_ext = ET.SubElement(ext, "gpxx:WaypointExtension")

        # add gpxx address
        address = ET.SubElement(wpt_ext, "gpxx:Address")
        ET.SubElement(address, "gpxx:StreetAddress").text = waypoint["name"]

        # add gpxx category when provided
        if category is not None:
            categories = ET.SubElement(wpt_ext, "gpxx:Categories")
            ET.SubElement(categories, "gpxx:Category").text = category

    return gpx


def add_waypoints_bounds(gpx, waypoints):
    metadata = ET.Element("metadata")
    ET.SubElement(metadata, "bounds", get_waypoints_bounds(waypoints))
    gpx.insert(0, metadata)


def write_gpx(gpx, filename):
    # indent XML and write to file
    ET.indent(gpx)
    tree = ET.ElementTree(gpx)
    tree.write(filename, encoding="UTF-8", xml_declaration=True)


def main():
    # get arguments
    args = get_arguments()

    # get first waypoint from each file
    waypoints = get_first_waypoints_from_files(args.files)

    # create gpx from waypoints
    gpx = create_gpx(waypoints, args.category, args.symbol)

    # add metadata with bounds
    if args.bounds:
        add_waypoints_bounds(gpx, waypoints)

    # write indented GPX to file
    write_gpx(gpx, args.output)


if __name__ == "__main__":
    main()
