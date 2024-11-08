"""
    AUTHOR:  Robin Trachsel
    VERSION: 1.0
    DATE:    08.11.2024

    DESCRIPTION: Main für die Flask Applikation der LB02
"""
from flask import Flask, jsonify, request
import os

app = Flask(__name__)


# A1G, A1F, A1E: Konzept der funktionalen Programmierung, Funktionen als Grundelemente.
# B2G, B2F, B2E: Funktionen als Objekte und Argumente (z.B. in der `apply_operation` Funktion)
def list_files(directory="."):
    """
    Listet alle Dateien in dem Directory
    B4G, B4F, B4E: Verwendung von Map und Filter, um Dateilisten zu transformieren.
    """
    files = os.listdir(directory)
    return list(filter(lambda f: os.path.isfile(os.path.join(directory, f)), files))


@app.route('/files', methods=['GET'])
def get_files():
    """
    Endpunkt um eine Liste von Dateien zu bekommen.
    C1G, C1F: Refactoring for better readability.
    """
    directory = request.args.get('directory', '.')
    try:
        files = list_files(directory)
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# B1G, B1F, B1E: Funktionen werden in kleine, funktionale Teile aufgeteilt
# zum Beispiel durch Funktionen wie `apply_operation`.
def apply_operation(files, operation):
    """Apply an operation (e.g., uppercase) to a list of files.
    B3G, B3F, B3E: Nutzung von Lambda-Ausdrücken zur Dateimanipulation.
    """
    if operation == "uppercase":
        return list(map(lambda f: f.upper(), files))
    elif operation == "lowercase":
        return list(map(lambda f: f.lower(), files))
    return files


@app.route('/files/transform', methods=['GET'])
def transform_files():
    """
    Endpoint to get transformed file names based on operation.
    A1F, A1G: Anwendungsbeispiel für das Konzept `immutable values`
    """
    directory = request.args.get('directory', '.')
    operation = request.args.get('operation', 'uppercase')
    try:
        files = list_files(directory)
        transformed_files = apply_operation(files, operation)
        return jsonify(transformed_files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# B2F, B2E: Higher-order functions, Funktionen als Argumente (Closures)
def advanced_filter(files, condition):
    """
    Filter files based on a condition.
    B3E: Lambda-Ausdrücke zum Sortieren und Filtern, Benutzerdefinierte Filterung
    """
    if condition == "large":
        return list(filter(lambda f: os.path.getsize(f) > 1024, files))  # Example: files > 1KB
    elif condition == "small":
        return list(filter(lambda f: os.path.getsize(f) <= 1024, files))
    return files


@app.route('/files/filter', methods=['GET'])
def filter_files():
    """
    Endpoint to filter files based on size condition.
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


# Rekursive Funktion, um in einem Verzeichnis und seinen Unterverzeichnissen nach einer bestimmten Datei zu suchen
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


# C1E: Auswirkungen des Refactorings bewerten und sicherstellen, dass keine Nebenwirkungen auftreten.
@app.route('/refactor_example', methods=['GET'])
def refactor_example():
    """
    Beispiel-Endpunkt, um Refactoring-Techniken zu demonstrieren.
    """
    data = {"message": "Refactored code example"}
    return jsonify(data)


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
