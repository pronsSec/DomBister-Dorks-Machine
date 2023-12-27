import argparse
from googlesearch import search
from flask import Flask, render_template
import ssl
import webbrowser
import threading

ssl._create_default_https_context = ssl._create_unverified_context

def open_browser():
      webbrowser.open_new("http://127.0.0.1:5000/")


app = Flask(__name__)

# Global variable to store results
global_results = {}

def google_search(query):
    try:
        results = []
        # Adjust the number of results and pause as needed, may need to adjust if there are issues with being ip banned 
        for j in search(query, num=10, stop=500, pause=4):
            results.append(j)
        return results
    except Exception as e:
        print(f"Error during search: {e}")
        return []

def run_dorks(dorks, targets):
    global global_results
    all_results = {}
    #print(all_results)
    for target in targets:
        for dork in dorks:
            query = f"{dork} site:{target}"
            print(f"Running dork '{dork}' on target '{target}'...")
            results = google_search(query)
            all_results[(target, dork)] = results
    global_results = all_results
    #print(all_results)
    return all_results

def save_and_print_results(results):
    with open('dork_results.txt', 'w') as file:
        for key, value in results.items():
            output = f"Results for {key[0]} with dork '{key[1]}':\n"
            print(output)
            file.write(output)
            for result in value:
                output = f"\tLink: {result}\n"
                print(output)
                file.write(output)
            print()
            file.write('\n')

def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

@app.route('/')
def index():
    return render_template('results.html', results=global_results)

def main():
    # ... [ASCII Art and Intro Text] ...
    ascii_name = r"""
     ____                  _     _     _            
    |  _ \  ___  _ __ ___ | |__ (_)___| |_ ___ _ __ 
    | | | |/ _ \| '_ ` _ \| '_ \| / __| __/ _ \ '__|
    | |_| | (_) | | | | | | |_) | \__ \ ||  __/ |   
    |____/ \___/|_| |_| |_|_.__/|_|___/\__\___|_|   
    """
    print(ascii_name)
    print("Welcome to the Google Dork Runner!")
    print("This tool runs a list of Google dorks against specified targets.")
    print("Results are printed and saved to 'dork_results.txt'.")
    print("\nNote: To mitigate the risk of IP banning, consider using 'proxychains4' for rotating proxies.")
    print("\nRunning the script...")
    

    parser = argparse.ArgumentParser(description='Run Google dorks on specified targets.')
    parser.add_argument('dorks_file', help='File containing Google dorks, one per line.')
    parser.add_argument('-t', '--target', help='Single target to run dorks against.')
    parser.add_argument('-tf', '--targets_file', help='File containing list of targets, one per line.')
    args = parser.parse_args()

    dorks = read_file(args.dorks_file)
    
    if args.targets_file:
        targets = read_file(args.targets_file)
    elif args.target:
        targets = [args.target]
    else:
        raise ValueError("No target or targets file provided.")

    results = run_dorks(dorks, targets)
    save_and_print_results(results)

if __name__ == '__main__':
    main()
    #input("\nPress Enter to start the web interface...")
    threading.Timer(1.25, open_browser).start()  # Waits for 1.25 seconds before opening the browser

    app.run(debug=False)  # Run Flask app in production mode
