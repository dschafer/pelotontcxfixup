from io import BytesIO, StringIO
import logging

from flask import Flask, flash, request, redirect, send_file
from werkzeug.utils import secure_filename

from fixup import fix_tcx

app = Flask(__name__)
logger = logging.getLogger(__name__)


def get_file(request):
    if "file" not in request.files:
        raise ValueError("No file provided.")
    file = request.files["file"]
    if "." not in file.filename:
        raise ValueError("File must be a .tcx file.")
    if file.filename.rsplit(".", 1)[1].lower() != "tcx":
        raise ValueError("File must be a .tcx file.")
    return file


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            file = get_file(request)
            logger.info("File successfully read.")
            logger.info(f"Filename was {secure_filename(file.filename)}.")
        except ValueError:
            logger.warn("Invalid file uploaded.")
            flash("Invalid file.")
            return redirect(request.url)

        in_string = str(file.stream.read(), encoding="utf-8")
        logger.info(f"File size is {len(in_string)}.")
        out_bytes_io = BytesIO()

        fix_tcx(StringIO(in_string), out_bytes_io)

        logger.info("TCX conversion complete.")
        logger.info(f"Output size is {out_bytes_io.getbuffer().nbytes}.")

        download_name = secure_filename(file.filename) + ".fixed.tcx"
        logger.info(f"Returning as {download_name}.")

        out_bytes_io.seek(0)
        return send_file(out_bytes_io, as_attachment=True, download_name=download_name)
    return """
    <!doctype html>
    <title>Fix Peloton TCX</title>
    <h1>Fix Peloton TCX</h1>
    <p>To get Peloton data into Garmin Connect, the easiest path is to connect Peloton and Strava via their built-in integration, then export the original TCX from Strava and import it into Garmin.</p>
    <p>Unfortunately, Garmin Connect won't correctly parse that TCX out of the box, because the TCX has some non-standard aspects to it.</p>
    <p>This script takes in one of those Peloton-to-Strava TCX files, fixes the aspects that Garmin Connect cannot handle, and produces a new TCX file for import into Garmin.</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value="Upload TCX File">
    </form>
    <p>Github source for this site and script: <a href="https://github.com/dschafer/pelotontcxfixup/">https://github.com/dschafer/pelotontcxfixup/</a></p>
    """
