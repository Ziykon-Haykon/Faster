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

const formReg = document.getElementById("formRegister");
const formLog = document.getElementById("formLogin");

formLog.onsubmit = function(e) {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    if (!email || !password) {
        alert("Заполните все поля!");
        return;
    }
    formLog.submit();
}

formReg.onsubmit = function(e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const age = document.getElementById("age").value;

    if (!name || !email || !password || !age) {
        alert("Заполните все поля!");
        return;
    }

    formReg.submit();
};