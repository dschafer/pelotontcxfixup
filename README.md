# Peloton TCX Fixup for Garmin

To get Peloton data into Garmin Connect, the easiest path is to connect Peloton and Strava via their built-in integration, then export the original TCX from Strava and import it into Garmin.

Unfortunately, Garmin Connect won't correctly parse that TCX out of the box, because the TCX has some non-standard aspects to it.

This script takes in one of those Peloton-to-Strava TCX files, fixes the aspects that Garmin Connect cannot handle, and produces a new TCX file for import into Garmin.

## Downloading the fixup script

You can download the fixup script directly from Github. Go to https://github.com/dschafer/pelotontcxfixup/blob/master/fixup.py and hit "command-shift-s", and "fixup.py" will get downloaded.

You can put this file wherever you want, but for the rest of this doc I will assume it is in your "Documents" folder.

## Downloading Peloton files from Strava

Now that you have the script downloaded, you need to download an activity from Peloton. Peloton doesn't let you do so directly, but Strava does... so if your Peloton activites appear in Strava, you can use Strava to get the activity file.

To do so, go to a Peloton activity in Strava and click the "three dots" icon on the bottom of the left-hand column. Once you do so, you'll see an option to "Export Original".

<img width="675" alt="export-original" src="https://github.com/dschafer/pelotontcxfixup/assets/2760005/b0f3e08c-573d-485d-9c1a-e37db6acfcdb">

When you click "Export Original", you'll see a .tcx file get downloaded.

## Command Line Usage

Now that you have that file, you can use the downloaded script on the command line. My activity file is in "Downloads" and the script is in "Documents", so I would open "Terminal" on my Mac, and run

```
python3 ~/Documents/fixup.py \
  < ~/Downloads/45_min_Power_Zone_Endurance_Ride_with_Matt_Wilpers.tcx \
  > ~/Downloads/45_min_Power_Zone_Endurance_Ride_with_Matt_Wilpers.tcx.fixed.tcx
```

Which says to run `~/Documents/fixup.py`, using `~/Downloads/45_min_Power_Zone_Endurance_Ride_with_Matt_Wilpers.tcx` as the input, and writing the output to `~/Downloads/45_min_Power_Zone_Endurance_Ride_with_Matt_Wilpers.tcx.fixed.tcx`

## Debugging

If you run into permissions issues, you might need to give Finder (for Quick Actions) or Terminal (for Command Line) full disk access. I found [these instructions](https://brianli.com/how-to-fix-automator-operation-not-permitted-error-in-macos-catalina/) clear, and will link to them rather than trying to rewrite them myself.
