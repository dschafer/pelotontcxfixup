# Peloton TCX Fixup for Garmin

To get Peloton data into Garmin Connect, the easiest path is to connect Peloton and Strava via their built-in integration, then export the original TCX from Strava and import it into Garmin.

Unfortunately, Garmin Connect won't correctly parse that TCX out of the box, because the TCX has some non-standard aspects to it.

This script takes in one of those Peloton-to-Strava TCX files, fixes the aspects that Garmin Connect cannot handle, and produces a new TCX file for import into Garmin.

## Downloading the fixup script

You can download the fixup script directly from Github. Go to https://github.com/dschafer/pelotontcxfixup/blob/master/fixup.py and hit **Command-Shift-s**, and `fixup.py` will get downloaded.

You can put this file wherever you want, but for the rest of this doc I will assume it is in your "Documents" folder.

## Downloading Peloton files from Strava

Now that you have the script downloaded, you need to download an activity from Peloton. Peloton doesn't let you do so directly, but Strava does... so if your Peloton activites appear in Strava, you can use Strava to get the activity file.

To do so, go to a Peloton activity in Strava and click the "three dots" icon on the bottom of the left-hand column. Once you do so, you'll see an option to "Export Original".

<img width="675" alt="export-original" src="https://github.com/dschafer/pelotontcxfixup/assets/2760005/b0f3e08c-573d-485d-9c1a-e37db6acfcdb">

When you click "Export Original", you'll see a .tcx file get downloaded.

## Command Line Usage

Now that you have that file, you can use the downloaded script on the command line. My activity file is in "Downloads" and the script is in "Documents", so I would open "Terminal" on my Mac, and run

```lang=bash
python3 ~/Documents/fixup.py \
  < ~/Downloads/45_min_Power_Zone_Endurance_Ride_with_Matt_Wilpers.tcx \
  > ~/Downloads/45_min_Power_Zone_Endurance_Ride_with_Matt_Wilpers.tcx.fixed.tcx
```

Which says to run `~/Documents/fixup.py`, using `~/Downloads/45_min_Power_Zone_Endurance_Ride_with_Matt_Wilpers.tcx` as the input, and writing the output to `~/Downloads/45_min_Power_Zone_Endurance_Ride_with_Matt_Wilpers.tcx.fixed.tcx`

## Quick Actions with Mac Automator

To use this without the terminal, you can create a "Quick Action" in Automator, and then use this by right-clicking on files in the future.

To do so, open "Automator". When it asks what type of document you want to create, choose a "Quick Action"

<img width="1112" alt="automator-new" src="https://github.com/dschafer/pelotontcxfixup/assets/2760005/50143a77-f595-4357-884b-45788fc50604">

Once you have your quick action, configure it to look like the following (updating the location of `fixup.py` to reflect wherever you put in earlier).

<img width="1112" alt="quick-action-in-automator" src="https://github.com/dschafer/pelotontcxfixup/assets/2760005/e9981212-28f1-4bab-b38a-ef65930c7312">

Importantly:

* The workflow should receive "files or folders" in "Finder"
* Inside "Run shell script", it should pass input "as arguments"
* The contents of the shell script should be

```lang=bash
for f in "$@"
do
	python3 ~/Documents/fixup.py \
      < "$f" \
      > "$f.fixed.tcx"
done
```

Once you've done so, save the quick action (I gave mine the name "Fix TCX") and edit automator.

Now, open Finder and go to the TCX file you downloaded. Right click, and you should see "Quick Actions > Fix TCX" as an option. Run that, and a new file that ends in ".tcx.fixed.tcx" should be created, right next to the original file.

<img width="999" alt="finder" src="https://github.com/dschafer/pelotontcxfixup/assets/2760005/909d421c-b01e-4a71-98f9-a44ed851a527">

## Debugging

If you run into permissions issues, you might need to give Finder (for Quick Actions) or Terminal (for Command Line) full disk access. I found [these instructions](https://brianli.com/how-to-fix-automator-operation-not-permitted-error-in-macos-catalina/) clear, and will link to them rather than trying to rewrite them myself.
