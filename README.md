# Peloton TCX Fixup for Garmin

**Quick start**: Go to https://dschafer.pythonanywhere.com/ which is a simple hosted version of this repository, and has all of the instructions there as well.

## Intro

To get Peloton data into Garmin Connect, the easiest path is to connect Peloton and Strava via their built-in integration, then export the original TCX from Strava and import it into Garmin.

Unfortunately, Garmin Connect won't correctly parse that TCX out of the box, because the TCX has some non-standard aspects to it.

This script takes in one of those Peloton-to-Strava TCX files, fixes the aspects that Garmin Connect cannot handle, and produces a new TCX file for import into Garmin.

## Instructions

### Downloading Peloton files from Strava

Peloton doesn't let you download TCX files directly, but Strava does... so if your Peloton activites appear in Strava, you can use Strava to get the activity file.

To do so, go to a Peloton activity in Strava and click the "three dots" icon on the bottom of the left-hand column. Once you do so, you'll see an option to "Export Original".

<img width="675" alt="A screenshot showing where the 'Export Original' option is on Strava." src="https://github.com/dschafer/pelotontcxfixup/assets/2760005/b0f3e08c-573d-485d-9c1a-e37db6acfcdb">

When you click "Export Original", you'll see a .tcx file get downloaded. If you try and upload this file to Garmin directly, it will fail, which is why the conversion script is needed. See the three options below on how to convert the file so you can upload it to Garmin.

### Using the hosted website (easy)

The simplest way to do the conversion is to go to https://dschafer.pythonanywhere.com/. That site hosts the script, and will allow you to upload the Peloton TCX file, and download the fixed version.

### Running Locally (intermediate)

You can download the fixup script directly from Github. Go to https://github.com/dschafer/pelotontcxfixup/blob/master/fixup.py and hit **Command-Shift-s**, and `fixup.py` will get downloaded.

You can put this file wherever you want, but for the rest of this doc I will assume it is in your "Documents" folder.

Now that you have that file, you can use the downloaded script on the command line. My activity file is in "Downloads" and the script is in "Documents", so I would open "Terminal" on my Mac, and run

```lang=bash
python3 ~/Documents/fixup.py \
  < ~/Downloads/45_min_Power_Zone_Endurance_Ride_with_Matt_Wilpers.tcx \
  > ~/Downloads/45_min_Power_Zone_Endurance_Ride_with_Matt_Wilpers.tcx.fixed.tcx
```

Which says to run `~/Documents/fixup.py`, using `~/Downloads/45_min_Power_Zone_Endurance_Ride_with_Matt_Wilpers.tcx` as the input, and writing the output to `~/Downloads/45_min_Power_Zone_Endurance_Ride_with_Matt_Wilpers.tcx.fixed.tcx`

### Adding a Quick Action (advanced)

To run this locally even faster, you can create a "Quick Action" in Automator, and then use this by right-clicking on files in the future.

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

### Debugging local usage

If you run into permissions issues, you might need to give Finder (for Quick Actions) or Terminal (for Command Line) full disk access. I found [these instructions](https://brianli.com/how-to-fix-automator-operation-not-permitted-error-in-macos-catalina/) clear, and will link to them rather than trying to rewrite them myself.
