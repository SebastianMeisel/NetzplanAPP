#!/usr/bin/env python3
import os                                                             # Zum Speichern
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory  # Webserver
from werkzeug.utils import secure_filename                            # Begrenze erlaubte Dateien 
from netzplan import Projekt, Netzplan                                # Generiere Netzplan


# Web-App initialisieren
app = Flask(__name__)

# Konfiguration
app.config['UPLOAD_FOLDER'] = "/home/sebastian/git/Netzplan_Upload/static/file/uploads" # Upload-Ordner für Datei-Upload
ALLOWED_EXTENSIONS = {'xlsx'}

# Funktion zum überprüfen. ob Dateityp erlaubt ist
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Funktion zum Verarbeiten des Dateiuploads
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('Datei gespeichert')
            ##### Netzplan aus Datei generieren

            P = Projekt(1, "Projekt")
            P.ImportiereVonExcel(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))

            NP = Netzplan("Projekt")
            NP.Zeichnen(P)
            NP.PdfExport(app.config['UPLOAD_FOLDER'])
            NP.JPGExport(app.config['UPLOAD_FOLDER'])
            P.ZeigeKritischenPfad()
            
            return render_template('netzplan.html')
            #return(request.url)
            #return redirect(url_for('download_file', name=filename))
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
