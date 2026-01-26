function showRegister() {
    const login = document.getElementById("login");
    const register = document.getElementById("register");
    if (login) login.classList.add("hidden");
    if (register) register.classList.remove("hidden");
}

function showLogin() {
    const register = document.getElementById("register");
    const login = document.getElementById("login");
    if (register) register.classList.add("hidden");
    if (login) login.classList.remove("hidden");
}

function initAuth() {
    const btnToLogin = document.querySelector('.IWannaLog');
    const btnToRegister = document.querySelector('.IWannaReg');
    if (btnToLogin) btnToLogin.addEventListener('click', (e) => { e.preventDefault(); showLogin(); });
    if (btnToRegister) btnToRegister.addEventListener('click', (e) => { e.preventDefault(); showRegister(); });

    // Handle form submissions
    const formRegister = document.getElementById('formRegister');
    const formLogin = document.getElementById('formLogin');

    if (formRegister) {
        formRegister.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            data.age = parseInt(data.age);
            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                if (response.ok) {
                    const html = await response.text();
                    document.body.innerHTML = html;
                    initAuth(); // Re-initialize after replacing content
                } else {
                    const error = await response.json();
                    alert('Error: ' + JSON.stringify(error));
                }
            } catch (error) {
                console.error('Error submitting form:', error);
            }
        });
    }

    if (formLogin) {
        formLogin.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                if (response.ok) {
                    const html = await response.text();
                    document.body.innerHTML = html;
                    initAuth(); // Re-initialize after replacing content
                    initHello();
                } else {
                    const error = await response.json();
                    alert('Error: ' + JSON.stringify(error));
                }
            } catch (error) {
                console.error('Error submitting form:', error);
            }
        });
    }

    console.log('auth script initialized', { btnToLogin, btnToRegister });
}

function initHello() {
    if (document.getElementById('addProductForm')) {
        function popupFn() {
            document.getElementById("overlay").style.display = "block";
            document.getElementById("popupDialog").style.display = "block";
        }

        function closeFn() {
            document.getElementById("overlay").style.display = "none";
            document.getElementById("popupDialog").style.display = "none";
        }

        document.getElementById("addProductForm").addEventListener("submit", async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch("/addProduct", {
                    method: "POST",
                    body: formData
                });
                
                if (response.ok) {
                    const product = await response.json();
                    addProductCard(product);
                    closeFn();
                    document.getElementById("addProductForm").reset();
                } else {
                    alert("Ошибка при добавлении товара");
                }
            } catch (error) {
                console.error("Ошибка:", error);
                alert("Ошибка при добавлении товара");
            }
        });

        function addProductCard(product) {
            const container = document.getElementById("productsContainer");
            
            const card = document.createElement("div");
            card.className = "product-card";
            card.innerHTML = `
                <div class="product-id">ID: ${product.id}</div>
                <div class="product-title">${product.title}</div>
                <div class="product-price">${product.price}₽</div>
            `;
            
            container.appendChild(card);
        }

        window.addEventListener("scroll", () => {
            if (window.scrollY >= 30) {
                document.body.classList.add("sticky-header");
            } else {
                document.body.classList.remove("sticky-header");
            }
        });

        // Add onclick to the button
        const addBtn = document.querySelector('button[onclick="popupFn()"]');
        if (addBtn) {
            addBtn.onclick = popupFn;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    initAuth();
    initHello();
});