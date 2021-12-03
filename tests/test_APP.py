# Tests mit verschiedenen Eingabedateien
import os
import pytest
from NetzplanAPP import create_app
from os.path import join, dirname, realpath
import html

# Client einrichten
@pytest.fixture
def client():
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client


# Hilfsfunktion        
def send_xlsx(client, Pfad: str):
    with open(Pfad, 'rb') as file:
        return client.post('/', data=dict(file=(file, file.name)), follow_redirects=True, content_type='multipart/form-data')

@pytest.mark.parametrize("datei,expected", [
    ("Projekt.xlsx", 'Netzplan-Download'),
    ("Projekt_Ohne_Ressourcen.xlsx", 'Netzplan-Download'),
    ("Projekt_Ohne_Ressourcen_und_ID_num.xlsx", 'Netzplan-Download'),
    ("Projekt_Ohne_Ressourcen_und_ID.xlsx", 'Spalte &#39;ID&#39; fehlt in der Tabelle &#39;Projekt&#39;!'),
    ("Projekt_Ohne_Ressourcen_und_ID_Dauer.xlsx", 'Spalte &#39;ID&#39; fehlt in der Tabelle &#39;Projekt&#39;!'),
    ("Projekt_Ohne_Projekt.xlsx", 'Tabelle &#39;Projekt&#39; fehlt oder hat den falschen Namen'),
    ("Ressourcen_Ohne_ID.xlsx", 'Spalte &#39;ID&#39; fehlt in der Tabelle &#39;Ressourcen&#39;!'),
])
    

def test_send_xlsx(client, datei, expected):

    # Ordentliche Testdatei
    Pfad = join(dirname(realpath(__file__)), datei)
    rv = send_xlsx(client, Pfad)
    assert expected in rv.data.decode('utf-8')

    
def test_keine_datei(client):
    # keine Datei
    rv = client.post('/', data=dict(file=''), follow_redirects=True, content_type='multipart/form-data')

    assert 'Keine Datei gewählt' in rv.data.decode('utf-8') # "Keine Datei gewählt"
    
