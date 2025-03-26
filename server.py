from flask import Flask, request, send_file, render_template, jsonify
import os
from Crypto.Cipher import AES, DES, ARC2
import base64
from stegano import lsb
from Crypto.Random import get_random_bytes

app = Flask(__name__)

# Create necessary directories
UPLOAD_FOLDER = 'uploads'
ENCRYPTED_FOLDER = 'encrypted'
KEYS_FOLDER = 'keys'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
os.makedirs(KEYS_FOLDER, exist_ok=True)

# AES, DES, RC2 Key (Must match the required length)
KEY = b'SixteenByteKey!!'  # 16 bytes for AES

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/encrypt_page')
def encrypt_page():
    return render_template('encrypt.html')

@app.route('/decrypt_page')
def decrypt_page():
    return render_template('decrypt.html')

def encrypt_data(data, method):
    """Encrypt data using AES, DES, or RC2"""
    if method == "AES":
        key = get_random_bytes(16)  # Generate a random 16-byte key
        cipher = AES.new(key, AES.MODE_EAX)
    elif method == "DES":
        key = get_random_bytes(8)  # Generate a random 8-byte key
        cipher = DES.new(key, DES.MODE_EAX)
    elif method == "RC2":
        key = get_random_bytes(8)  # Generate a random 8-byte key
        cipher = ARC2.new(key, ARC2.MODE_EAX)
    else:
        return None, None

    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + ciphertext, base64.b64encode(key).decode()

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    try:
        file = request.files['file']
        method = request.form['method']
        
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            encrypted_filepath = os.path.join(ENCRYPTED_FOLDER, file.filename + ".enc")
            stego_image_path = os.path.join(KEYS_FOLDER, "key_image.png")
            sample_image_path = "static/sample.png"

            # Check if the sample image exists
            if not os.path.exists(sample_image_path):
                return "Sample image for steganography is missing. Please add 'static/sample.png'."

            file_data = file.read()
            encrypted_data, encryption_key = encrypt_data(file_data, method)

            if encrypted_data:
                with open(encrypted_filepath, 'wb') as f:
                    f.write(encrypted_data)

                # Combine the encryption method and key, then hide in the image
                secret_message = f"{method}:{encryption_key}"
                print(f"Embedding secret message: {secret_message}")  # Debugging
                secret_image = lsb.hide(sample_image_path, secret_message)
                secret_image.save(stego_image_path)

                # Serve both files for download
                return jsonify({
                    "encrypted_file": f"/download?file={encrypted_filepath}",
                    "stego_image": f"/download?file={stego_image_path}"
                })
            else:
                return "Invalid encryption method."
        else:
            return "No file uploaded."
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    """Extract key from image and decrypt the file"""
    key_image = request.files['stego_image']
    encrypted_file = request.files['encrypted_file']

    if key_image and encrypted_file:
        key_image_path = os.path.join(KEYS_FOLDER, "uploaded_key.png")
        encrypted_file_path = os.path.join(ENCRYPTED_FOLDER, encrypted_file.filename)

        key_image.save(key_image_path)
        encrypted_file.save(encrypted_file_path)

        # Extract the secret message (method:key) from the image
        secret_message = lsb.reveal(key_image_path)

        if not secret_message:
            return "Failed to extract key from the image. The stego image may be corrupted or invalid.", 400

        try:
            method, encryption_key = secret_message.split(":")
            decoded_key = base64.b64decode(encryption_key)
        except Exception as e:
            return f"Invalid secret message format: {str(e)}", 400

        print(f"Extracted secret message: {secret_message}")  # Debugging

        if secret_message:
            try:
                method, encryption_key = secret_message.split(":")
                decoded_key = base64.b64decode(encryption_key)

                with open(encrypted_file_path, 'rb') as f:
                    encrypted_data = f.read()

                nonce = encrypted_data[:16]  # Extract nonce
                ciphertext = encrypted_data[16:]

                # Decrypt based on the encryption method
                if method == "AES":
                    cipher = AES.new(decoded_key, AES.MODE_EAX, nonce=nonce)
                elif method == "DES":
                    cipher = DES.new(decoded_key, DES.MODE_EAX, nonce=nonce)
                elif method == "RC2":
                    cipher = ARC2.new(decoded_key, ARC2.MODE_EAX, nonce=nonce)
                else:
                    return "Unsupported encryption method.", 400

                decrypted_data = cipher.decrypt(ciphertext)

                decrypted_file_path = os.path.join(UPLOAD_FOLDER, "decrypted_" + encrypted_file.filename)
                with open(decrypted_file_path, 'wb') as f:
                    f.write(decrypted_data)

                # Serve the decrypted file for download
                return send_file(decrypted_file_path, as_attachment=True)
            except Exception as e:
                return f"Decryption failed: {str(e)}", 400
        else:
            return "Failed to extract key from the image.", 400

    return "No file uploaded.", 400

@app.route('/download')
def download_file():
    """Serve a file for download"""
    file_path = request.args.get('file')
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found.", 404

if __name__ == '__main__':
    app.run(debug=True)
