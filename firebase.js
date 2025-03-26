// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, onAuthStateChanged, signOut }
from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

// Firebase Configuration
const firebaseConfig = {
    apiKey: "AIzaSyCJYXmHRou5VcYUw2VsjPbInCc3nnf8OuQ",
    authDomain: "crptknight-5b9b8.firebaseapp.com",
    projectId: "crptknight-5b9b8",
    storageBucket: "crptknight-5b9b8.appspot.com",
    messagingSenderId: "677198930089",
    appId: "1:677198930089:web:cc7988d157e500bf9f89b8"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Function to register a user
window.registerUser = function() {
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;

    if (!email || !password) {
        alert("Please enter both email and password.");
        return;
    }

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            alert("Registration successful! You can now log in.");
            console.log("User registered:", userCredential.user.email);
        })
        .catch((error) => {
            alert("Registration failed: " + error.message);
            console.error("Error during registration:", error);
        });
};

// Function to log in a user
window.loginUser = function() {
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    if (!email || !password) {
        alert("Please enter both email and password.");
        return;
    }

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            alert("Login successful!");
            console.log("User logged in:", userCredential.user.email);

            // Hide login/register fields and show "Get Started"
            document.getElementById("auth-container").style.display = "none";
            document.getElementById("get-started").style.display = "block";
        })
        .catch((error) => {
            alert("Login failed: " + error.message);
            console.error("Error during login:", error);
        });
};

// Function to check if user is already logged in
onAuthStateChanged(auth, (user) => {
    if (user) {
        console.log("User is logged in:", user.email);
        document.getElementById("auth-container").style.display = "none";
        document.getElementById("get-started").style.display = "block";
    } else {
        console.log("No user logged in.");
    }
});

// Function to redirect to index.html after login
window.redirectToApp = function() {
    onAuthStateChanged(auth, (user) => {
        if (user) {
            window.location.href = "/index";
        } else {
            alert("Please log in first!");
        }
    });
};

// Function to log out a user
window.logoutUser = function() {
    signOut(auth)
        .then(() => {
            alert("Logout successful!");
            window.location.href = "/"; // Redirect to the homepage
        })
        .catch((error) => {
            alert("Logout failed: " + error.message);
        });
};
