import argparse
import requests
from bs4 import BeautifulSoup
import time
from flask import Flask, render_template

app = Flask(__name__)

# Global variable to store results
global_results = {}

def google_search(query):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def parse_results(soup):
    results = []
    for g in soup.find_all('div', class_='g'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text if g.find('h3') else ''
            results.append({'title': title, 'link': link})
    return results

def run_dorks(dorks, targets):
    global global_results
    all_results = {}
    for target in targets:
        for dork in dorks:
            query = f"{dork} site:{target}"
            print(f"Running dork '{dork}' on target '{target}'...")
            soup = google_search(query)
            results = parse_results(soup)
            all_results[(target, dork)] = results
    global_results = all_results
    return all_results

def save_and_print_results(results):
    with open('dork_results.txt', 'w') as file:
        for key, value in results.items():
            output = f"Results for {key[0]} with dork '{key[1]}':\n"
            print(output)
            file.write(output)
            for result in value:
                output = f"\tTitle: {result['title']}, Link: {result['link']}\n"
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

    input("\nPress Enter to view the results in a web interface...")
    app.run(debug=True)

if __name__ == '__main__':
    main()
