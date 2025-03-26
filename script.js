document.getElementById('encryptForm').addEventListener('submit', async function (event) {
    event.preventDefault();
    
    let fileInput = document.getElementById('fileInput').files[0];
    let encryptionMethod = document.getElementById('encryptionMethod').value;

    if (!fileInput) {
        alert("Please select a file to encrypt.");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput);
    formData.append("method", encryptionMethod);

    try {
        let response = await fetch('/encrypt', { method: "POST", body: formData });
        let result = await response.json();

        if (result.encrypted_file && result.stego_image) {
            alert("Encryption successful! Files are ready for download.");

            // Automatically download the encrypted file
            let encryptedFileLink = document.createElement('a');
            encryptedFileLink.href = result.encrypted_file;
            encryptedFileLink.download = ''; // Let the browser handle the filename
            document.body.appendChild(encryptedFileLink);
            encryptedFileLink.click();
            document.body.removeChild(encryptedFileLink);

            // Automatically download the stego image
            let stegoImageLink = document.createElement('a');
            stegoImageLink.href = result.stego_image;
            stegoImageLink.download = ''; // Let the browser handle the filename
            document.body.appendChild(stegoImageLink);
            stegoImageLink.click();
            document.body.removeChild(stegoImageLink);
        } else {
            alert("Encryption failed: " + result);
        }
    } catch (error) {
        alert("An error occurred: " + error.message);
    }
});

document.getElementById('decryptForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    let stegoImageInput = document.getElementById('stegoImageInput').files[0];
    let encryptedFileInput = document.getElementById('encryptedFileInput').files[0];

    if (!stegoImageInput || !encryptedFileInput) {
        alert("Please select both the stego image and the encrypted file.");
        return;
    }

    let formData = new FormData();
    formData.append("stego_image", stegoImageInput);
    formData.append("encrypted_file", encryptedFileInput);

    try {
        let response = await fetch('/decrypt', { method: "POST", body: formData });

        if (response.ok) {
            // Create a blob from the response
            let blob = await response.blob();

            // Create a temporary download link
            let downloadLink = document.createElement('a');
            downloadLink.href = window.URL.createObjectURL(blob);
            downloadLink.download = 'decrypted_file'; // Default filename
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);

            alert("Decryption successful! File has been downloaded.");
        } else {
            let errorMessage = await response.text();
            alert("Decryption failed: " + errorMessage);
        }
    } catch (error) {
        alert("An error occurred: " + error.message);
    }
});
