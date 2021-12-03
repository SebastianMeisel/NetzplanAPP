import os
import pytest
from NetzplanAPP import create_app
from os.path import join, dirname, realpath
import html

@pytest.fixture
def client():
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client


def send_xlsx(client, Pfad: str):
    with open(Pfad, 'rb') as file:
        return client.post('/', data=dict(file=(file, file.name)), follow_redirects=True, content_type='multipart/form-data')


    

def test_send_xlsx(client):

    # Ordentliche Testdatei
    Pfad = join(dirname(realpath(__file__)),"Projekt.xlsx")
    rv = send_xlsx(client, Pfad)
    assert b'Netzplan-Download' in rv.data

    # Ordentliche Testdatei ohne Ressourcen
    Pfad = join(dirname(realpath(__file__)),"Projekt_Ohne_Ressourcen.xlsx")
    rv = send_xlsx(client, Pfad)
    assert b'Netzplan-Download' in rv.data

    #  Testdatei ohne Ressourcen und ID - korrekte (numerische) Verweise
    Pfad = join(dirname(realpath(__file__)),"Projekt_Ohne_Ressourcen_und_ID_korr.xlsx")
    rv = send_xlsx(client, Pfad)
    assert b'Netzplan-Download' in rv.data

    
    #  Testdatei ohne Ressourcen und ID - falsche Verweise
    Pfad = join(dirname(realpath(__file__)),"Projekt_Ohne_Ressourcen_und_ID.xlsx")
    rv = send_xlsx(client, Pfad)
    assert b'Spalte &#39;ID&#39; fehlt in der Tabelle &#39;Projekt&#39;!' in rv.data

    # Testdatei ohne Ressourcen und ID
    Pfad = join(dirname(realpath(__file__)),"Projekt_Ohne_Ressourcen_und_ID_Dauer.xlsx")
    rv = send_xlsx(client, Pfad)
    assert b'Spalte &#39;ID&#39; fehlt in der Tabelle &#39;Projekt&#39;!' in rv.data

    # Testdatei ohne Projekt-Tabelle
    Pfad = join(dirname(realpath(__file__)),"Projekt_Ohne_Projekt.xlsx")
    rv = send_xlsx(client, Pfad)
    assert b'Tabelle &#39;Projekt&#39; fehlt oder hat den falschen Namen' in rv.data


    # Testdatei ohne Ressourcen-ID
    Pfad = join(dirname(realpath(__file__)),"Ressourcen_Ohne_ID.xlsx")
    rv = send_xlsx(client, Pfad)
    assert b'Spalte &#39;ID&#39; fehlt in der Tabelle &#39;Ressourcen&#39;!' in rv.data

    

    # keine Datei
    rv = client.post('/', data=dict(file=''), follow_redirects=True, content_type='multipart/form-data')

    assert 'Keine Datei gewÃ¤hlt' in rv.data.decode('utf-8') # "Keine Datei gewählt"
    
