# Peloton TCX Fixup for Garmin

To get Peloton data into Garmin Connect, the easiest path is to connect Peloton and Strava via their built-in integration, then export the original TCX from Strava and import it into Garmin.

Unfortunately, Garmin Connect won't correctly parse that TCX out of the box, because the TCX has some non-standard aspects to it.

This script takes in one of those Peloton-to-Strava TCX files, fixes the aspects that Garmin Connect cannot handle, and produces a new TCX file for import into Garmin.
