const tg = window.Telegram.WebApp;

let currentUserId = null;

// Функція, яка виконається ТІЛЬКИ після повної готовності Telegram WebApp
tg.ready(() => {
    tg.expand();

    // Ініціалізуємо дані користувача строго всередині готовності
    if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
        const user = tg.initDataUnsafe.user;
        currentUserId = user.id;
        document.getElementById('username-display').innerText = user.first_name + (user.last_name ? ' ' + user.last_name : '');
        document.getElementById('user-id-display').innerText = user.id;
    } else {
        // Якщо тестуємо в браузері
        currentUserId = 123456789;
        document.getElementById('username-display').innerText = "Vergil (Тестовий Профіль)";
        document.getElementById('user-id-display').innerText = currentUserId;
    }

    // Запускаємо завантаження товарів ТІЛЬКИ після того, як визначили ID юзера
    loadProducts();
});

// 1. Завантаження товарів для витрини магазину
async function loadProducts() {
    const container = document.getElementById('products-container');
    try {
        const response = await fetch('/api/products');
        if (!response.ok) throw new Error(`Помилка: ${response.status}`);

        const products = await response.json();

        if (!products || products.length === 0) {
            container.innerHTML = `<p style="text-align: center; color: var(--hint-color); padding: 20px;">Наразі в магазині немає товарів.</p>`;
            return;
        }

        let html = '';
        products.forEach(prod => {
            html += `
                <div class="product-card">
                    <div class="product-name">${prod.name}</div>
                    <div class="product-desc">${prod.description}</div>
                    <div class="product-footer">
                        <div class="product-price">${prod.price.toFixed(2)} UAH</div>
                        <button class="buy-btn" onclick="buyProduct(${prod.id}, '${prod.name}')">Купити</button>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;
    } catch (error) {
        console.error("Помилка при завантаженні товарів:", error);
        container.innerHTML = `<p style="text-align: center; color: #ff4d4d; padding: 20px;">❌ Не вдалося завантажити товари.</p>`;
    }
}

// 2. Загрузка даних користувача з БД
async function loadDbUserData() {
    if (!currentUserId) return;
    const dbField = document.getElementById('db-username-field');

    try {
        const response = await fetch(`/api/user_data?id=${currentUserId}`);
        if (response.ok) {
            const data = await response.json();
            if (data.username) {
                dbField.innerHTML = `🔑 <b>БД Никнейм:</b> @${data.username}`;
            } else {
                dbField.innerHTML = `🔑 <b>БД Никнейм:</b> немає`;
            }
        } else {
            dbField.innerHTML = `<span style="color: var(--hint-color);">Користувача немає в БД</span>`;
        }
    } catch (error) {
        console.error("Помилка отримання даних користувача з БД:", error);
    }
}

// 3. Загрузка покупок користувача з БД
async function loadDbPurchases() {
    if (!currentUserId) return;
    const container = document.getElementById('purchases-container');

    try {
        const response = await fetch(`/api/purchase?id=${currentUserId}`);
        if (!response.ok) throw new Error(`Статус: ${response.status}`);

        const purchases = await response.json();

        if (!purchases || purchases.length === 0) {
            container.innerHTML = `<p style="color: var(--hint-color);">Ви ще не придбали жодного товару.</p>`;
            return;
        }

        let htmlContent = '';
        purchases.forEach(itemName => {
            htmlContent += `
                <div class="purchase-item" style="border-left: 3px solid var(--button-color); padding-left: 8px; margin-bottom: 8px; text-align: left;">
                    📦 <b>${itemName}</b> <br>
                    <span style="font-size: 11px; color: var(--hint-color);">Статус: Оплачено (Синхронізовано з БД)</span>
                </div>
            `;
        });
        container.innerHTML = htmlContent;
    } catch (error) {
        console.error("Помилка завантаження покупок з БД:", error);
        container.innerHTML = `<p style="color: #ff4d4d;">❌ Не вдалося завантажити історію покупок.</p>`;
    }
}

// 4. Переключення вкладок
function switchTab(tab) {
    const shopTab = document.getElementById('shop-tab');
    const profileTab = document.getElementById('profile-tab');
    const btnShop = document.getElementById('btn-shop');
    const btnProfile = document.getElementById('btn-profile');

    if (tab === 'shop') {
        shopTab.style.display = 'block';
        profileTab.style.display = 'none';
        btnShop.classList.add('active');
        btnProfile.classList.remove('active');
    } else if (tab === 'profile') {
        shopTab.style.display = 'none';
        profileTab.style.display = 'block';
        btnShop.classList.remove('active');
        btnProfile.classList.add('active');

        loadDbUserData();
        loadDbPurchases();
    }
}

// 5. Логіка купівлі
function buyProduct(productId, productName) {
    try {
        const data = {
            action: "buy",
            product_id: productId,
            product_name: productName
        };
        tg.sendData(JSON.stringify(data));
        tg.close();
    } catch (error) {
        alert("Помилка отправки даних боту: " + error.message);
    }
}