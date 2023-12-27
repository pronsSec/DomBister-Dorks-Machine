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

def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

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
    ascii_name = r"""
     ____                  _     _     _            
    |  _ \  ___  _ __ ___ | |__ (_)___| |_ ___ _ __ 
    | | | |/ _ \| '_ ` _ \| '_ \| / __| __/ _ \ '__|
    | |_| | (_) | | | | | | |_) | \__ \ ||  __/ |   
    |____/ \___/|_| |_| |_|_.__/|_|___/\__\___|_|   
    """
    print(ascii_name)
    print("Welcome to the Google Dork Runner!")
    print("This tool runs a list of Google dorks against specified targets. \nIf no dorks list or single dork is provided a default list will be used.")
    print("Results are printed and saved to 'dork_results.txt' and displayed in the auto-refreshing web interface.")
    print("\nNote: To mitigate the risk of IP banning, consider using 'proxychains4' for rotating proxies.")
    print("\nRunning the script...")

    parser = argparse.ArgumentParser(description='Run Google dorks on specified targets.')
    parser.add_argument('-d', '--dorks_file', help='File containing Google dorks, one per line.', default=None)
    parser.add_argument('-t', '--target', help='Single target to run dorks against.')
    parser.add_argument('-tf', '--targets_file', help='File containing list of targets, one per line.')
    args = parser.parse_args()

    if args.dorks_file:
        dorks = read_file(args.dorks_file)
    else:
        # Use the default dorks file
        dorks = read_file(DEFAULT_DORKS_FILE)

    if args.targets_file:
        targets = read_file(args.targets_file)
    elif args.target:
        targets = [args.target]
    else:
        raise ValueError("No target or targets file provided.")

    # Start the dork processing in a separate thread
    dork_thread = threading.Thread(target=process_dorks, args=(dorks, targets))
    dork_thread.start()

if __name__ == '__main__':
    main()
    threading.Timer(1.25, open_browser).start()  # Waits for 1.25 seconds before opening the browser
    app.run(debug=False)  # Run Flask app in production mode
