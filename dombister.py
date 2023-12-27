import argparse
from googlesearch import search
from flask import Flask, render_template
import ssl
import webbrowser
import threading
from threading import Lock

ssl._create_default_https_context = ssl._create_unverified_context

# Default dorks file
DEFAULT_DORKS_FILE = "default_dorks.txt"

app = Flask(__name__)

# Global variable to store results and a lock for thread safety
global_results = {}
results_lock = Lock()

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

def google_search(query):
    try:
        results = []
        for j in search(query, num=10, stop=500, pause=4):
            results.append(j)
        return results
    except Exception as e:
        print(f"Error during search: {e}")
        return []

def process_dorks(dorks, targets):
    global global_results
    for target in targets:
        for dork in dorks:
            query = f"{dork} site:{target}"
            print(f"Running dork '{dork}' on target '{target}'...")
            results = google_search(query)
            with results_lock:
                global_results[(target, dork)] = results

@app.route('/')
def index():
    with results_lock:
        return render_template('results.html', results=global_results)

def main():
    # ... [ASCII Art and Intro Text and Argument Parsing] ...

    dork_thread = threading.Thread(target=process_dorks, args=(dorks, targets))
    dork_thread.start()

if __name__ == '__main__':
    main()
    threading.Timer(1.25, open_browser).start()  # Waits for 1.25 seconds before opening the browser
    app.run(debug=False)  # Run Flask app in production mode
