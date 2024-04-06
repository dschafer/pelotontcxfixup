# Peloton TCX Fixup for Garmin

To get Peloton data into Garmin Connect, the easiest path is to connect Peloton and Strava via their built-in integration, then export the original TCX from Strava and import it into Garmin.

Unfortunately, Garmin Connect won't correctly parse that TCX out of the box, because the TCX has some non-standard aspects to it.

This script takes in one of those Peloton-to-Strava TCX files, fixes the aspects that Garmin Connect cannot handle, and produces a new TCX file for import into Garmin.

## Downloading Peloton files from Strava

This assumes you have Peloton and Strava connected, so that your Peloton activites appear in Strava.

If that's the case, you can go to a Peloton activity and click the "three dots" icon on the bottom of the left-hand column. Once you do so, you'll see an option to "Export Original".

<img width="675" alt="export-original" src="https://github.com/dschafer/pelotontcxfixup/assets/2760005/b0f3e08c-573d-485d-9c1a-e37db6acfcdb">

When you click that, you'll see a .tcx file get downloaded.
