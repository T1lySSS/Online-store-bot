const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();


if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
    const user = tg.initDataUnsafe.user;
    document.getElementById('username-display').innerText = user.first_name + (user.last_name ? ' ' + user.last_name : '');
    document.getElementById('user-id-display').innerText = user.id;
} else {
    document.getElementById('username-display').innerText = "Vergil (Тестовий Профіль)";
    document.getElementById('user-id-display').innerText = "777000123";
}


function switchTab(tab) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

    if (tab === 'shop') {
        document.getElementById('shop-tab').classList.add('active');
        document.getElementById('btn-shop').classList.add('active');
    } else if (tab === 'profile') {
        document.getElementById('profile-tab').classList.add('active');
        document.getElementById('btn-profile').classList.add('active');
        loadPurchases();
    }
}


function buyProduct(productId, productName) {
    try {
        let myPurchases = JSON.parse(localStorage.getItem('user_purchases')) || [];
        if (!myPurchases.includes(productName)) {
            myPurchases.push(productName);
            localStorage.setItem('user_purchases', JSON.stringify(myPurchases));
        }

        const data = {
            action: "buy",
            product_id: productId,
            product_name: productName
        };

        tg.sendData(JSON.stringify(data));
        tg.close();
    } catch (error) {
        alert("Помилка: " + error.message);
    }
}


function loadPurchases() {
    const container = document.getElementById('purchases-container');
    let myPurchases = JSON.parse(localStorage.getItem('user_purchases')) || [];

    if (myPurchases.length === 0) {
        container.innerHTML = `<p style="color: var(--hint-color);">Ви ще не придбали жодного товару.</p>`;
        return;
    }

    let htmlContent = '';
    myPurchases.forEach(item => {
        htmlContent += `
            <div class="purchase-item" style="border-left: 3px solid var(--button-color); padding-left: 8px; margin-bottom: 8px;">
                📦 <b>${item}</b> <br>
                <span style="font-size: 11px; color: var(--hint-color);">Статус: Оплачено (Цифровий доступ надано)</span>
            </div>
        `;
    });

    container.innerHTML = htmlContent;
}