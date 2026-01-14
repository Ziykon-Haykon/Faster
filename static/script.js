const login = document.getElementById("login");
const register = document.getElementById("register");

function showRegister() {
    login.classList.add("hidden");
    register.classList.remove("hidden");
}

function showLogin() {
    register.classList.add("hidden");
    login.classList.remove("hidden");
}