#!/usr/bin/python3

import sys
from typing import TextIO, BinaryIO
import xml.etree.ElementTree as ET

ET.register_namespace("", "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2")
ns = {
    "tcd": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
    "ae": "http://www.garmin.com/xmlschemas/ActivityExtension/v2",
}


def round_xpath_to_int(root: ET.Element, xpath: str) -> None:
    """Given an xpath, replace the float value inside with a rounded int value"""
    for e in root.findall(xpath, ns):
        e.text = str(int(float(str(e.text))))


def fix_tcx(infile: TextIO, outfile: BinaryIO) -> None:
    """Fixes a TCX file from Peloton to be spec compliant"""
    root = ET.fromstring(infile.read().strip())
    tree = ET.ElementTree(root)

    # Remove the creator tag, Garmin won't recognize that
    activity = root.find("./tcd:Activities/tcd:Activity", ns)
    if not activity:
        raise ValueError("No activity found")
    creator = activity.find("./tcd:Creator", ns)
    if not creator:
        raise ValueError("No creator found")
    try:
        activity.remove(creator)
    except Exception:
        pass

    # The only valid sports are Running, Cycling, and Other.
    # Peloton exports Biking, and Garmin will read that.
    if activity.get("Sport") not in ["Running", "Cycling", "Biking", "Other"]:
        activity.set("Sport", "Other")

    # Round these values to ints, since Garmin requires that
    round_xpath_to_int(root, ".//ae:Watts")
    round_xpath_to_int(root, ".//tcd:AverageHeartRateBpm/tcd:Value")
    round_xpath_to_int(root, ".//tcd:MaximumHeartRateBpm/tcd:Value")
    round_xpath_to_int(root, ".//tcd:HeartRateBpm/tcd:Value")
    round_xpath_to_int(root, ".//tcd:Calories")
    round_xpath_to_int(root, ".//tcd:Cadence")

    # Output to stdout
    tree.write(outfile, encoding="UTF-8", xml_declaration=True)


def main():
    fix_tcx(sys.stdin, sys.stdout.buffer)


if __name__ == "__main__":
    main()
