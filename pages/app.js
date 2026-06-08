
let userId = 123456789;
let userUsername = "Браузерний користувач";
let tg = null;

function initializeApp() {

    if (window.Telegram && window.Telegram.WebApp) {
        tg = window.Telegram.WebApp;


        tg.ready();
        tg.expand();


        if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
            userId = tg.initDataUnsafe.user.id;
            userUsername = tg.initDataUnsafe.user.username || `User_${userId}`;
        }
    } else {
        console.log("Додаток запущено поза межами Telegram Mini App. Використовуємо дефолтні дані.");
    }


    loadProducts();
}


if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}


function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

    if (tabName === 'market') {
        document.getElementById('tab-market').classList.add('active');
        document.getElementById('btn-market').classList.add('active');
    } else if (tabName === 'profile') {
        document.getElementById('tab-profile').classList.add('active');
        document.getElementById('btn-profile').classList.add('active');
        loadUserProfile();
    }
}


async function loadProducts() {
    const container = document.getElementById('products-container');
    if (!container) return;

    try {
        const response = await fetch('/api/products');
        if (!response.ok) throw new Error(`Помилка сервера: ${response.status}`);

        const products = await response.json();

        if (!products || products.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: gray; margin-top: 20px;">Наразі товарів немає.</p>';
            return;
        }

        let html = '';
        products.forEach(prod => {
            html += `
                <div class="product-card">
                    <h3 style="margin: 0 0 8px 0; font-size: 18px;">${prod.name}</h3>
                    <p style="color: #666; font-size: 14px; margin: 0 0 12px 0;">${prod.description}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <b style="color: #007bc1; font-size: 16px;">${prod.price.toFixed(2)} UAH</b>
                        <button onclick="sendBuyAction(${prod.id}, '${prod.name}')" style="padding: 8px 16px; background: #007bc1; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-weight: bold;">Купити</button>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;
    } catch (e) {
        console.error(e);
        container.innerHTML = `<p style="text-align: center; color: red; margin-top: 20px;">❌ Не вдалося завантажити товари.</p>`;
    }
}


function sendBuyAction(productId, productName) {
    if (tg) {
        const dataToSend = {
            action: "buy",
            product_id: productId,
            product_name: productName
        };

        tg.sendData(JSON.stringify(dataToSend));
        tg.close();
    } else {
        alert(`Емуляція купівлі в браузері: ${productName} (ID: ${productId})`);
    }
}


async function loadUserProfile() {
    document.getElementById('profile-name').innerText = userUsername;
    document.getElementById('profile-id').innerText = `ID: ${userId}`;

    const purchasesContainer = document.getElementById('purchases-container');
    purchasesContainer.innerHTML = '<p style="text-align: center; color: gray;">Завантаження покупок...</p>';

    try {
        const response = await fetch(`/api/profile?telegram_id=${userId}&username=${encodeURIComponent(userUsername)}`);
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
                    <div style="font-size: 12px; color: #8e8e93; margin-top: 4px;">Статус: Доступ надано</div>
                </div>
            `;
        });
        purchasesContainer.innerHTML = html;

    } catch (e) {
        console.error(e);
        purchasesContainer.innerHTML = `<p style="text-align: center; color: red;">❌ Помилка синхронізації з БД.</p>`;
    }
}