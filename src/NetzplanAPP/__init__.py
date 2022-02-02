#!/usr/bin/env python3
import os  # Zum Speichern
from os.path import join, dirname, realpath
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)  # Webserver
from werkzeug.utils import secure_filename  # Begrenze erlaubte Dateien
from netzplan.netzplan import Projekt, Netzplan  # Generiere Netzplan

# Activate Logging
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("netzplan.log")
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
# werkzeug logger nur in Console
werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.addHandler(stream_handler)

# Create an App
def create_app(test_config=None):
    # Web-App initialisieren
    app = Flask(__name__, instance_relative_config=True)
    ALLOWED_EXTENSIONS = {"xlsx"}

    # Konfiguration
    app.config.from_mapping(
        SECRET_KEY="dev",
        UPLOAD_FOLDER=join(
            dirname(realpath(__file__)), "./static/file/uploads"
        ),  # Upload-Ordner für Datei-Upload
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Funktion zum überprüfen. ob Dateityp erlaubt ist
    def allowed_file(filename):
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    # Funktion zum Verarbeiten des Dateiuploads
    @app.route("/", methods=["GET", "POST"])
    def upload_file():
        # LÃ¶sche verwaist eDateien im Upload-Ordner
        for file in os.listdir(app.config["UPLOAD_FOLDER"]):
            os.unlink(os.path.join(app.config["UPLOAD_FOLDER"], file))
        if request.method == "POST":
            # Überprüfe, ob Daei ausgewählt wurde
            if "file" not in request.files:
                logger.warning("Keine Datei gewählt")
                return render_template(
                    "index.html", error_message="Keine Datei gewählt"
                )
            file = request.files["file"]
            # Dateiname darf kein leere String sein
            if file.filename == "":
                logger.warning("Keine Datei gewählt")
                return render_template(
                    "index.html", error_message="Keine Datei gewählt"
                )
            # Nur weiterarbeiten, wenn der Dateiname "sicher" ist
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                ##### Netzplan aus Datei generieren
                P = Projekt(1, "Projekt")
                error_message = P.ImportiereVonExcel(
                    str(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                )

                if error_message != "":
                    return render_template("index.html", error_message=error_message)

                # LÃ¶sche Pdf
                os.unlink(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                # Ausgabedateien erstellen
                NP = Netzplan("Projekt")
                NP.Zeichnen(P)
                NP.PdfExport(app.config["UPLOAD_FOLDER"])
                NP.JPGExport(app.config["UPLOAD_FOLDER"])

                return render_template("netzplan.html")
            else:
                logger.warning("Dateiname falsch")
                return render_template(
                    "index.html", error_message="Bitte Dateinamen ändern!"
                )

        return render_template("index.html")

    @app.route("/uploads/<name>")
    def download_file(name):
        return send_from_directory(app.config["UPLOAD_FOLDER"], name)

    return app
