#!/usr/bin/env python3
import os                                                             # Zum Speichern
from flask import Flask, render_template, request, redirect, url_for, send_from_directory  # Webserver
from werkzeug.utils import secure_filename                            # Begrenze erlaubte Dateien 
from netzplan import Projekt, Netzplan                                # Generiere Netzplan


# Web-App initialisieren
app = Flask(__name__)

# Konfiguration
app.config['UPLOAD_FOLDER'] = "./static/file/uploads" # Upload-Ordner für Datei-Upload
ALLOWED_EXTENSIONS = {'xlsx'}

# Funktion zum überprüfen. ob Dateityp erlaubt ist
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Funktion zum Verarbeiten des Dateiuploads
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Überprüfe, ob Daei ausgewählt wurde
        if 'file' not in request.files:
            return render_template('index.html', error_message='Keine Datei gewählt')
        file = request.files['file']
        # Dateiname darf kein leere String sein
        if file.filename == '':
            return render_template('index.html', error_message='Keine Datei gewählt')
        # Nur weiterarbeiten, wenn der Dateiname "sicher" ist
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            ##### Netzplan aus Datei generieren
            P = Projekt(1, "Projekt")
            error_message = P.ImportiereVonExcel(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))

            if error_message != "":
                return render_template('index.html', error_message=error_message)
                

            NP = Netzplan("Projekt")
            NP.Zeichnen(P)
            NP.PdfExport(app.config['UPLOAD_FOLDER'])
            NP.JPGExport(app.config['UPLOAD_FOLDER'])
            
            return render_template('netzplan.html')
        else:
            return render_template('index.html', error_message='Bitte Dateinamen ändern!')

    return render_template('index.html')




@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
    
if __name__ == "__main__":
    app.secret_key = '#äre9023lflsäpäeopsr0lkn<o8z8z3hcl'
    app.config['SESSION_TYPE'] = 'filesystem'

    #sess.init_app(app)

    app.debug = True
    app.run()
