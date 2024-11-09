"""
    AUTHOR:  Robin Trachsel
    VERSION: 1.0
    DATE:    08.11.2024

    DESCRIPTION: Main für die Flask Applikation der LB02
"""
from flask import Flask, jsonify, request
import os

app = Flask(__name__)


# B2G, B2F, B2E: Funktionen als Objekte und Argumente (z.B. in der `apply_operation` Funktion)
# B3E: Verwendung von Lambda-Ausdrücken, um den Programmfluss zu steuern (z.B. durch Sortieren von Listen basierend auf benutzerdefinierten Kriterien)
# B4G, B4F, B4E: Verwendung von Map, Filter und Reduce, um komplexe Datenverarbeitungsaufgaben zu lösen
def list_files(directory="."):
    """
    Listet alle Dateien in dem Directory.
    B4G, B4F, B4E: Map und Filter wird verwendet, um eine Liste von Dateien zu erzeugen und Filterbedingungen anzuwenden.
    """
    files = os.listdir(directory)
    return list(filter(lambda f: os.path.isfile(os.path.join(directory, f)), files))


@app.route('/files', methods=['GET'])
def get_files():
    """
    Endpunkt um eine Liste von Dateien zu bekommen.
    C1G, C1F: Refactoring-Techniken verwendet, um den Code lesbarer zu machen.
    """
    directory = request.args.get('directory', '.')
    try:
        files = list_files(directory)
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# B3G, B3F, B3E: Lambda-Ausdrücke verwenden, um eine einzelne oder mehrere Operationen durchzuführen
def apply_operation(files, operation):
    """
    Wandelt Dateinamen entsprechend der angegebenen Operation (uppercase/lowercase) um.
    B3G, B3F: Einfache Lambda-Ausdrücke und komplexere Lambda-Ausdrücke, die mehrere Argumente verarbeiten.
    """
    if operation == "uppercase":
        return list(map(lambda f: f.upper(), files))
    elif operation == "lowercase":
        return list(map(lambda f: f.lower(), files))
    return files


@app.route('/files/transform', methods=['GET'])
def transform_files():
    """
    Endpoint um Dateinamen basierend auf der angegebenen Operation zu transformieren.
    B1G, B1F, B1E: Funktionen werden in kleine, funktionale Teile aufgeteilt.
    """
    directory = request.args.get('directory', '.')
    operation = request.args.get('operation', 'uppercase')
    try:
        files = list_files(directory)
        transformed_files = apply_operation(files, operation)
        return jsonify(transformed_files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# B2F, B2E: Higher-Order Functions und Closures verwenden (z.B. in der `advanced_filter` Funktion)
def advanced_filter(files, condition):
    """
    Filtert die Dateien basierend auf einer Bedingung (z.B. "large" oder "small").
    B2F, B2E: Closures werden verwendet, um eine flexiblere Filterung zu ermöglichen.
    """
    if condition == "large":
        return list(filter(lambda f: os.path.getsize(f) > 1024, files))  # Dateien > 1KB
    elif condition == "small":
        return list(filter(lambda f: os.path.getsize(f) <= 1024, files))  # Dateien <= 1KB
    return files


@app.route('/files/filter', methods=['GET'])
def filter_files():
    """
    Endpoint um Dateien basierend auf der Grösse zu filtern.
    A1E: Vergleich des funktionalen mit dem prozeduralen Paradigma in der Praxis.
    """
    directory = request.args.get('directory', '.')
    condition = request.args.get('condition', 'large')
    try:
        files = list_files(directory)
        filtered_files = advanced_filter(files, condition)
        return jsonify(filtered_files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# C1E: Auswirkungen des Refactorings auf den Code bewerten und sicherstellen, dass keine unerwünschten Nebeneffekte auftreten.
@app.route('/refactor_example', methods=['GET'])
def refactor_example():
    """
    Beispiel-Endpunkt, um Refactoring-Techniken zu demonstrieren.
    Refactoring-Techniken helfen, den Code lesbarer und wartungsfreundlicher zu gestalten.
    """
    data = {"message": "Refactored code example"}
    return jsonify(data)


# B4G, B4F, B4E: Anwendung von Map, Filter und Reduce zur Verarbeitung und Manipulation von Daten
@app.route('/files/process', methods=['GET'])
def process_files():
    """
    Endpunkt zur Verarbeitung und Transformation von Dateien mit verschiedenen Operationen.
    B2E: Funktionen als Argumente weitergeben und flexibel anwenden (z.B. in apply_operation und advanced_filter).
    B4G, B4F: Nutzung von Map, Filter und Reduce zur Manipulation von Daten.
    """
    directory = request.args.get('directory', '.')
    filename = request.args.get('filename', None)
    condition = request.args.get('condition', None)
    operation = request.args.get('operation', None)

    files = list_files(directory) if not filename else [search_file(directory, filename)]
    if condition:
        files = advanced_filter(files, condition)
    if operation:
        files = apply_operation(files, operation)

    return jsonify(files)


# Rekursive Funktion zur Datei-Suche
def search_file(directory, filename):
    """
    Sucht rekursiv nach einer Datei in einem Verzeichnis und dessen Unterverzeichnissen.
    """
    try:
        for entry in os.listdir(directory):
            path = os.path.join(directory, entry)
            if os.path.isfile(path) and entry == filename:
                return path
            elif os.path.isdir(path):
                # Rekursiver Aufruf der Funktion, um auch Unterverzeichnisse zu durchsuchen
                result = search_file(path, filename)
                if result:
                    return result
    except Exception as e:
        print(f"Fehler beim Zugriff auf {directory}: {e}")
    return None


@app.route('/files/search', methods=['GET'])
def search_file_endpoint():
    """
    Endpoint, um nach einer bestimmten Datei in einem Verzeichnis und dessen Unterverzeichnissen zu suchen.
    """
    directory = request.args.get('directory', '.')
    filename = request.args.get('filename', '')
    if not filename:
        return jsonify({"error": "filename parameter is required"}), 400

    try:
        result = search_file(directory, filename)
        if result:
            return jsonify({"file_path": result})
        else:
            return jsonify({"message": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
