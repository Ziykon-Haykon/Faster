const login = document.getElementById("login");
const register = document.getElementById("register");

function showRegister() {
    if (login) login.classList.add("hidden");
    if (register) register.classList.remove("hidden");
}

function showLogin() {
    if (register) register.classList.add("hidden");
    if (login) login.classList.remove("hidden");
}

window.showRegister = showRegister;
window.showLogin = showLogin;

document.addEventListener('DOMContentLoaded', () => {
    const btnToLogin = document.querySelector('.IWannaLog');
    const btnToRegister = document.querySelector('.IWannaReg');
    if (btnToLogin) btnToLogin.addEventListener('click', (e) => { e.preventDefault(); showLogin(); });
    if (btnToRegister) btnToRegister.addEventListener('click', (e) => { e.preventDefault(); showRegister(); });
    console.log('auth script initialized', { login, register, btnToLogin, btnToRegister });
});