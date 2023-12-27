# DomBister-Dorks-Machine

![DALL·E 2023-12-26 07 14 34 - Comic book style illustration of a person using Google dorks for penetration testing  The character is seated at a desk, smoking, with a focused, inte](https://github.com/pronsSec/DomBister-Dorks-Machine/assets/93559326/7dbb310d-7beb-4aef-83ca-680e51a58ce6)



## Introduction
The Google Dork Runner is a Python-based tool designed to automate the process of running Google dorks against specified targets. It provides both a command-line interface and a Flask-based web GUI for viewing results. This tool is intended for cybersecurity professionals and ethical hackers to assess the exposure of sensitive information on the web.

## Setup
### Requirements:
- Python 3.x
- Flask
- google

### Installation:
1. **Clone the repository:**
- git clone https://github.com/pronsSec/DomBister-Dorks-Machine

2. **Navigate to the cloned directory:**
- cd DomBister-Dorks-Machine

3. **Install the required Python packages:**
- pip install -r requirements.txt


## Usage
1. Prepare your dorks file (`dorks.txt`) with one dork per line. If you do not provide a single dork or target the tool will use a default list curated by myself.
2. If you have multiple targets, prepare a targets file (`targets.txt`) with one target per line.
3. Run the script:

python dombister.py dorks.txt -tf targets.txt

![Uploading Screenshot 2023-12-27 at 6.27.01 AM.png…]()


Or use `-t [target]` for a single target.

4. You will be able to view real-time results in the web interface (`http://127.0.0.1:5000/`).

### Web Interface:
- The web interface displays the results in a user-friendly format automatically.

## Ethical Use
This tool is created for educational and ethical use only. Users are responsible for adhering to all applicable laws and regulations, including respecting the terms of service of search engines and websites. The authors are not responsible for misuse or for any damages resulting from the use of this tool.

## Contributing
Contributions to the Google Dork Runner are welcome. To contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes.
4. Push to the branch.
5. Create a new Pull Request.


## Contact
For any queries or suggestions, please contact [Your Contact Information]

## Acknowledgments
- Thanks to the Python community for the invaluable resources.
- Special thanks to all contributors of this project.




