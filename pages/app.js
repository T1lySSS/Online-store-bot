let userId = 123456789;
let userUsername = "Браузерний користувач";

window.addEventListener('DOMContentLoaded', () => {
    try {
        const tg = window.Telegram.WebApp;
        tg.ready();
        tg.expand();


        if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
            const user = tg.initDataUnsafe.user;
            userId = user.id;
            userUsername = user.username || `${user.first_name} ${user.last_name || ''}`.trim();
        }

        else if (tg.initData) {
            const urlParams = new URLSearchParams(tg.initData);
            const userString = urlParams.get('user');
            if (userString) {
                const user = JSON.parse(userString);
                userId = user.id;
                userUsername = user.username || `${user.first_name} ${user.last_name || ''}`.trim();
            }
        }
    } catch (err) {
        console.error("Помилка Telegram WebApp:", err);
    }

    try {
        const nameElem = document.getElementById('profile-name');
        const idElem = document.getElementById('profile-id');
        if (nameElem) nameElem.innerText = userUsername;
        if (idElem) idElem.innerText = `ID: ${userId}`;
    } catch (err) {
        console.error("Помилка відображення профілю:", err);
    }

    loadProducts();
});

async function loadProducts() {
    const container = document.getElementById('products-container');
    if (!container) return;

    container.innerHTML = '<p style="text-align: center; color: gray;">Завантаження товарів...</p>';

    try {
        const response = await fetch('/api/products');
        if (!response.ok) throw new Error(`Статус: ${response.status}`);

        const products = await response.json();

        if (!products || products.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: gray;">Каталог порожній.</p>';
            return;
        }

        let html = '';
        products.forEach(p => {

            const priceInCents = Math.round(p.price * 100);
            html += `
                <div class="product-card">
                    <h3>${p.name}</h3>
                    <p>${p.description}</p>
                    <div class="product-footer">
                        <span class="price">${p.price.toFixed(2)} UAH</span>
                        <button class="buy-btn" onclick="buyProduct(${p.id}, '${p.name}', ${priceInCents})">Купити</button>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;

    } catch (err) {
        console.error("Помилка при завантаженні товарів:", err);
        container.innerHTML = '<p style="text-align: center; color: red;">Не вдалося завантажити товари.</p>';
    }
}

async function loadUserProfile() {
    const nameElem = document.getElementById('profile-name');
    const idElem = document.getElementById('profile-id');
    const purchasesContainer = document.getElementById('purchases-container');

    if (nameElem) nameElem.innerText = userUsername;
    if (idElem) idElem.innerText = `ID: ${userId}`;
    if (!purchasesContainer) return;

    purchasesContainer.innerHTML = '<p style="text-align: center; color: gray;">Завантаження покупок...</p>';

    try {
        const url = `/api/profile?telegram_id=${userId}&username=${encodeURIComponent(userUsername)}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Статус: ${response.status}`);

        const data = await response.json();

        if (!data.purchases || data.purchases.length === 0) {
            purchasesContainer.innerHTML = '<p style="text-align: center; color: gray;">Ви ще не придбали жодного товару.</p>';
            return;
        }

        let html = '';
        data.purchases.forEach(title => {
            html += `
                <div class="purchase-item">
                    <strong>📦 ${title}</strong>
                    <div style="font-size: 12px; color: #4cd964; margin-top: 4px; font-weight: bold;">Статус: Доступ надано</div>
                </div>
            `;
        });
        purchasesContainer.innerHTML = html;

    } catch (err) {
        console.error("Помилка в loadUserProfile:", err);
        purchasesContainer.innerHTML = `<p style="text-align: center; color: red;">Помилка синхронізації з БД.</p>`;
    }
}

function buyProduct(id, name, price) {
    try {
        const tg = window.Telegram.WebApp;
        if (tg) {
            const data = {
                action: "buy",
                product_id: id,
                product_name: name,
                price: price
            };
            tg.sendData(JSON.stringify(data));


            setTimeout(() => {
                tg.close();
            }, 500);
        }
    } catch (err) {
        console.error("Помилка при купівлі:", err);
    }
}

function switchTab(tabName) {
    const marketTab = document.getElementById('tab-market');
    const profileTab = document.getElementById('tab-profile');
    const marketBtn = document.getElementById('btn-market');
    const profileBtn = document.getElementById('btn-profile');

    if (tabName === 'market') {
        if (marketTab) marketTab.style.display = 'block';
        if (profileTab) profileTab.style.display = 'none';

        if (marketBtn) marketBtn.classList.add('active');
        if (profileBtn) profileBtn.classList.remove('active');

        loadProducts();
    } else if (tabName === 'profile') {
        if (marketTab) marketTab.style.display = 'none';
        if (profileTab) profileTab.style.display = 'block';

        if (marketBtn) marketBtn.classList.remove('active');
        if (profileBtn) profileBtn.classList.add('active');

        loadUserProfile();
    }
}