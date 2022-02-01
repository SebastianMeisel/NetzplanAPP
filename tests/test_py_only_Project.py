#!/usr/bin/env python3
from netzplan import Projekt, Netzplan
import hashlib


def sha256sum(filename):
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def test_project(capsys):
    ###################################################################
    # Beispiel

    P1 = Projekt(1, "Beispiel")

    # Arbeits-Pakete: Bezeichnung, Aufwand, ID (optional)
    P1.NeuesArbeitsPaket("Anfangen", 5, "1.1.1"),
    P1.NeuesArbeitsPaket("Weitermachen", 7, "1.1.2")
    P1.NeuesArbeitsPaket("Einkaufen", 1, "1.1.3")
    P1.NeuesArbeitsPaket("Ganz anders weitermachen", 4, "1.2.2")
    P1.NeuesArbeitsPaket("Aufhören", 7, "1.2.3")
    P1.NeuesArbeitsPaket("Anders weitermachen", 5, "1.2.1")
    P1.NeuesArbeitsPaket("Pause", 8, "1.3.1")
    P1.NeuesArbeitsPaket("Erholung", 6, "1.3.2")
    P1.NeuesArbeitsPaket("Feiern", 6, "1.3.3")

    # Abhängigkeiten
    P1.ArbeitsPakete["1.1.2"].Folgt("1.1.1")
    P1.ArbeitsPakete["1.1.3"].Folgt("1.1.2")
    P1.ArbeitsPakete["1.2.1"].Folgt("1.1.1")
    P1.ArbeitsPakete["1.2.2"].Folgt("1.2.1")
    P1.ArbeitsPakete["1.2.3"].Folgt("1.2.2")
    P1.ArbeitsPakete["1.3.1"].Folgt("1.2.1")
    P1.ArbeitsPakete["1.3.2"].Folgt("1.3.1")
    P1.ArbeitsPakete["1.3.3"].Folgt(
        ["1.1.3", "1.2.3", "1.3.2"]
    )  # Mehrere Arbeitspackete in einer Liste
    # (in eckigen Klammern) zusammenfassen
    ################################################################################
    # Ressourcen: Name
    P1.NeueRessource("FM", "Frank Müller")
    P1.NeueRessource("PL", "Pipi Langstrumpf")

    # Hr. Meier:  Ressource, Arbeitspacket, Kapazität (Default 100%)
    P1.RessourceZuweisen("FM", "1.1.1")
    P1.RessourceZuweisen("FM", "1.1.2", 50)
    P1.RessourceZuweisen("FM", "1.2.1", 50)
    P1.RessourceZuweisen("FM", "1.2.3")
    P1.RessourceZuweisen("FM", "1.1.3")
    P1.RessourceZuweisen("FM", "1.3.2")
    P1.RessourceZuweisen("FM", "1.3.3")

    # Pipi: Ressource, Arbeitspacket, Kapazität (Default 100%)
    P1.RessourceZuweisen("PL", "1.1.1")
    P1.RessourceZuweisen("PL", "1.1.3")
    P1.RessourceZuweisen("PL", "1.2.1")
    P1.RessourceZuweisen("PL", "1.2.2", 50)
    P1.RessourceZuweisen("PL", "1.3.1", 50)
    P1.RessourceZuweisen("PL", "1.3.2")
    P1.RessourceZuweisen("PL", "1.3.3")

    # Netzplan: Name der PDF
    N1 = Netzplan("Netzplan")
    N1.Zeichnen(P1)
    N1.PdfExport()
    N1.JPGExport()

    # Generiere MD5-Hash
    sum = sha256sum("Netzplan.jpg")
    assert sum == "6fd9f9b93a71a3512c0ab6368fa3ee5fc5a68c25b16ba7268d4daa356d4b409c"

    # Kristischen Pfad ausgeben
    P1.ZeigeKritischenPfad()
    assert (
        capsys.readouterr().out
        == "Kritischer Pfad: [ 1.1.1  - 1.2.1  - 1.3.1  - 1.3.2  - 1.3.3 ]\n"
    )
