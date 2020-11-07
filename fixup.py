#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET
ET.register_namespace('', 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2');

ns = {
  'tcd': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
  'ae': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'
}

def round_xpath_to_int(root, xpath):
  """Given an xpath, replace the float value inside with a rounded int value"""
  for e in root.findall(xpath, ns):
    e.text = str(int(float(e.text)))

def main():
  """
  Reads a TCX file from Strava that Peloton uploaded, and modifies it
  so that Garmin Connect will correctly parse it.
  """
  # Read the file from stdin
  tree = ET.parse(sys.stdin)
  root = tree.getroot()

  # Remove the creator tag, Garmin won't recognize that
  activity = root.find('./tcd:Activities/tcd:Activity', ns)
  creator = activity.find('./tcd:Creator', ns)
  activity.remove(creator)

  # The only valid sports are Running, Cycling, and Other.
  # Peloton exports Biking, and Garmin will read that.
  if activity.get('Sport') not in ['Running', 'Cycling', 'Biking', 'Other']:
    activity.set('Sport', 'Other')

  # Round these values to ints, since Garmin requires that
  round_xpath_to_int(root, './/ae:Watts')
  round_xpath_to_int(root, './/tcd:AverageHeartRateBpm/tcd:Value')
  round_xpath_to_int(root, './/tcd:MaximumHeartRateBpm/tcd:Value')
  round_xpath_to_int(root, './/tcd:HeartRateBpm/tcd:Value')
  round_xpath_to_int(root, './/tcd:Calories')
  round_xpath_to_int(root, './/tcd:Cadence')

  # Output to stdout
  tree.write(sys.stdout, encoding="UTF-8", xml_declaration=True)

if __name__ == "__main__":
  main()
