"""
    AUTHOR:  Robin Trachsel
    VERSION: 1.0
    DATE:    08.11.2024

    BESCHREIBUNG: Hauptprogramm für die Flask Applikation der LB02
"""
from flask import Flask, jsonify, request
import os

app = Flask(__name__)


# A1G, A1F, A1E: Konzept der funktionalen Programmierung, Funktionen als Grundelemente.
# B2G, B2F, B2E: Funktionen als Objekte und Argumente (z.B. in der `apply_operation` Funktion).
def list_files(directory="."):
    """
    Listet alle Dateien im angegebenen Verzeichnis auf.
    B4G, B4F, B4E: Verwendung von Map und Filter, um Dateilisten zu transformieren.
    """
    files = os.listdir(directory)
    return list(filter(lambda f: os.path.isfile(os.path.join(directory, f)), files))


@app.route('/files', methods=['GET'])
def get_files():
    """
    Endpunkt, um eine Liste von Dateien zu erhalten.
    C1G, C1F: Refactoring, um den Code besser lesbar zu machen.
    """
    directory = request.args.get('directory', '.')
    try:
        files = list_files(directory)
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# B1G, B1F, B1E: Funktionen werden in kleine, funktionale Einheiten aufgeteilt,
# zum Beispiel durch Funktionen wie `apply_operation`.

def apply_operation(files, operation):
    """
    Wendet eine Operation (z.B. Großschreibung) auf eine Liste von Dateien an.
    B3G, B3F, B3E: Nutzung von Lambda-Ausdrücken zur Manipulation von Dateien.
    """
    if operation == "uppercase":
        return list(map(lambda f: f.upper(), files))
    elif operation == "lowercase":
        return list(map(lambda f: f.lower(), files))
    return files


@app.route('/files/transform', methods=['GET'])
def transform_files():
    """
    Endpunkt, um transformierte Dateinamen basierend auf einer Operation zu erhalten.
    A1F, A1G: Beispielanwendung für das Konzept `immutable values`.
    """
    directory = request.args.get('directory', '.')
    operation = request.args.get('operation', 'uppercase')
    try:
        files = list_files(directory)
        transformed_files = apply_operation(files, operation)
        return jsonify(transformed_files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# B2F, B2E: Higher-Order-Funktionen, Funktionen als Argumente (Closures).
def advanced_filter(files, condition):
    """
    Filtert Dateien basierend auf einer Bedingung.
    B3E: Lambda-Ausdrücke zum Sortieren und Filtern, benutzerdefinierte Filterung.
    """
    if condition == "large":
        return list(filter(lambda f: os.path.getsize(f) > 1024, files))  # Beispiel: Dateien > 1KB
    elif condition == "small":
        return list(filter(lambda f: os.path.getsize(f) <= 1024, files))
    return files


@app.route('/files/filter', methods=['GET'])
def filter_files():
    """
    Endpunkt, um Dateien basierend auf einer Größenbedingung zu filtern.
    A1E: Vergleich von funktionalem und prozeduralem Paradigma in der Praxis.
    """
    directory = request.args.get('directory', '.')
    condition = request.args.get('condition', 'large')
    try:
        files = list_files(directory)
        filtered_files = advanced_filter(files, condition)
        return jsonify(filtered_files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# C1E: Auswirkungen des Refactorings bewerten und sicherstellen, dass keine unerwünschten Nebenwirkungen auftreten.
@app.route('/refactor_example', methods=['GET'])
def refactor_example():
    """
    Beispiel-Endpunkt, um Refactoring-Techniken zu demonstrieren.
    """
    data = {"message": "Refactored code example"}
    return jsonify(data)


# Startet die Flask-App
if __name__ == '__main__':
    app.run(debug=True)
