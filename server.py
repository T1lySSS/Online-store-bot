from aiohttp import web
from db.requests import get_all_products, get_user_purchases, get_user_data
import os


async def handle_get_products(request):
    try:
        products_data = get_all_products()
        return web.json_response(products_data)
    except Exception as ex:
        print(f"❌ Помилка в handle_get_products: {ex}")
        return web.json_response({"error": str(ex)}, status=500)


async def handle_index(request):
    path_to_index = os.path.join('pages', 'index.html')
    if os.path.exists(path_to_index):
        return web.FileResponse(path_to_index)
    return web.Response(text="index.html не знайдено в папці pages", status=404)


async def handle_user_purchase(request):
    telegram_id = request.rel_url.query.get('id')
    if not telegram_id:
        return web.json_response({"error": "Data not found"}, status=400)
    try:
        telegram_id = int(telegram_id)
    except:
        return web.json_response({"error": "Convert data error"}, status=400)
    try:
        purchase = get_user_purchases(telegram_id)
        return web.json_response(purchase)
    except Exception as ex:
        return web.json_response({"error": str(ex)}, status=500)


async def handle_user_data(request):
    telegram_id = request.rel_url.query.get('id')
    if not telegram_id:
        return web.json_response({"error": "Data not found"}, status=400)
    try:
        telegram_id = int(telegram_id)
    except Exception as ex:
        return web.json_response({"error": "Convert data error"}, status=400)

    try:
        user = get_user_data(telegram_id)
        if user:
            return web.json_response({
                "telegram_id": int(user.telegram_id),
                "username": str(user.username) if user.username else ""
            })
        else:
            return web.json_response({"error": "User not found"}, status=404)
    except Exception as ex:
        print(f"❌ Помилка в handle_user_data: {ex}")
        return web.json_response({"error": str(ex)}, status=500)


def make_app():
    app = web.Application()

    # 1. Спочатку реєструємо точні API-ендпоінти
    app.router.add_get('/api/products', handle_get_products)
    app.router.add_get('/api/purchase', handle_user_purchase)
    app.router.add_get('/api/user_data', handle_user_data)

    # 2. Головна сторінка
    app.router.add_get('/', handle_index)

    # 3. Статику підключаємо окремо, щоб вона не перекривала корінь '/'
    # Тепер у index.html файли підключатимуться як src="/pages/app.js" або src="/pages/styles.css"
    app.router.add_static('/pages/', path='pages', name='static')

    return app


if __name__ == '__main__':
    app = make_app()
    print("🚀 API та веб-сервер запущені на http://localhost:8000")
    web.run_app(app, host='localhost', port=8000)