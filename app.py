from io import BytesIO, StringIO
import logging
from xml.etree.ElementTree import ParseError

from flask import Flask, Request, flash, render_template, request, redirect, send_file
from werkzeug import Response
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from fixup import fix_tcx

app = Flask(__name__, template_folder=".")
app.config.from_pyfile("config.cfg")
logger = logging.getLogger(__name__)


def get_file(request: Request) -> FileStorage:
    """Returns the file from the request, or throws ValueError indicating an error."""
    if "file" not in request.files:
        raise ValueError("No file provided.")
    file = request.files["file"]
    filename = str(file.filename)
    if not filename:
        raise ValueError("No file provided.")
    if len(filename) <= 4 or filename[-4:] != ".tcx":
        raise ValueError("File must be a .tcx file.")
    return file


def flash_and_redirect(request: Request, error_str: str) -> Response:
    logger.warn(error_str)
    flash(error_str)
    return redirect(request.url)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            file = get_file(request)
        except ValueError as e:
            return flash_and_redirect(request, f"Invalid file uploaded: {str(e)}")
        filename = secure_filename(str(file.filename))
        logger.debug(f"File {filename} successfully uploaded.")

        try:
            in_string = str(file.stream.read(), encoding="utf-8")
        except UnicodeDecodeError:
            return flash_and_redirect(
                request, "Invalid file uploaded: file was not a UTF-8 text file."
            )
        logger.debug(f"Input size is {len(in_string)}.")

        logger.debug("Starting TCX conversion.")
        out_bytes_io = BytesIO()
        try:
            fix_tcx(StringIO(in_string), out_bytes_io)
        except ParseError:
            return flash_and_redirect(
                request,
                "Invalid file uploaded: file was not a valid TCX XML doducment.",
            )
        out_bytes_io.seek(0)
        logger.debug("TCX conversion complete.")
        logger.debug(f"Output size is {out_bytes_io.getbuffer().nbytes}.")

        download_name = filename[:-4] + "_Fixed.tcx"
        logger.info(f"Conversion of {filename} complete, returning as {download_name}.")
        return send_file(out_bytes_io, as_attachment=True, download_name=download_name)
    return render_template("./index.html.jinja")
