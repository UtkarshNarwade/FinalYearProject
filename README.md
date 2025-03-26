
Secure File Using Hybrid Cryptography

A robust web application designed for secure file encryption and decryption using a hybrid cryptographic approach. The system integrates AES, DES, and RC2 encryption algorithms, coupled with steganography to securely embed encryption keys within images. Users can upload files for encryption, store the encryption key inside an image, and later retrieve it for decryption and secure file access.

Tech Stack & Architecture

🔹 Backend:
✅ Flask (Python Web Framework) – Manages routes, API handling, and cryptographic processes.
✅ PyCryptodome – Implements AES, DES, and RC2 encryption for data security.
✅ Stegano – Facilitates steganographic embedding of encryption keys within images.
✅ Flask-MySQL (if using MySQL) – Handles structured data storage and retrieval.

🔹 Frontend:
✅ HTML, CSS, JavaScript – Provides an intuitive and responsive user interface.
✅ Firebase SDK – Enables seamless authentication and user management.

🔹 Authentication & Database:
✅ Firebase Authentication – Secure user authentication for login and registration.
✅ MySQL (XAMPP) – Stores encrypted metadata and user-related information (if applicable).

🔹 Development Tools:
✅ VS Code – Primary IDE for development and debugging.

Key Features

✔ Hybrid Cryptography: AES, DES, and RC2 encryption for enhanced data security.
✔ Steganographic Key Storage: Encryption keys are hidden within images for additional security.
✔ Secure Authentication: Firebase authentication ensures only authorized access.
✔ User-Friendly Interface: A clean and interactive web UI for seamless encryption and decryption operations.

This project leverages modern cryptographic principles and secure authentication to provide a confidential file storage and retrieval system.



Steps to Execute: 

## Prerequisites
- Python 3.9 or later
- Flask
- Firebase account for authentication
- Node.js (optional, for advanced frontend development)

## Installation and Setup

### For Windows
1. Install Python from [python.org](https://www.python.org/).
2. Clone or download the project:
   ```cmd
   git clone <repository_url>
   cd SecureFileEncryption



   3. Create and activate a virtual environment:

   python -m venv venv
venv\Scripts\activate

4. install dependencies
pip install -r requirements.txt

5. run flask server
python server.py

6. open browser and navigate to

http://127.0.0.1:5000





----------- for linux-----------------



1. Install Python:
sudo apt update
sudo apt install python3 python3-venv python3-pip


2. Clone or download the project:
git clone <repository_url>
cd SecureFileEncryption


3. Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate


4. Install dependencies:
pip install -r requirements.txt

5. Run the Flask server:
python server.py  or python3 server.py



6. open browser and paste:
http://127.0.0.1:5000






=========

for new user and new firebase:

firebase setup:

Create a Firebase project at Firebase Console.
Enable Email/Password Authentication in the Firebase Authentication settings.
Replace the Firebase configuration in static/js/firebase.js with your Firebase project's configuration.
File Structure
templates/: Contains HTML templates.
static/css/: Contains CSS files for styling.
static/js/: Contains JavaScript files, including Firebase integration.
server.py: Flask server script.
requirements.txt: Python dependencies.
Usage
Open the application in a browser.
Register or log in using your email and password.
Use the "Get Started" button to access the main application.
Notes
Ensure the static/sample.png file exists for steganography.
Update the Firebase configuration in static/js/firebase.js before running the application.
