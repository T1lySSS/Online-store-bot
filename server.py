import os
import time
from aiohttp import web
from db.requests import get_all_products, get_user_purchases, register_user

async def handle_index(request):
    path_to_index = os.path.join('pages', 'index.html')
    if os.path.exists(path_to_index):
        with open(path_to_index, 'r', encoding='utf-8') as f:
            html_content = f.read()


        cache_buster = str(int(time.time()))
        html_content = html_content.replace('src="/pages/app.js"', f'src="/pages/app.js?v={cache_buster}"')
        html_content = html_content.replace('href="/pages/styles.css"', f'href="/pages/styles.css?v={cache_buster}"')

        return web.Response(text=html_content, content_type='text/html')
    return web.Response(text="index.html не знадено в папці pages", status=404)


async def handle_get_products(request):
    try:

        products = await get_all_products()
        return web.json_response(products)
    except Exception as ex:
        print(f"Помилка в handle_get_products: {ex}")
        return web.json_response({"error": str(ex)}, status=500)


async def handle_get_profile(request):
    try:
        telegram_id_str = request.query.get('telegram_id')
        username = request.query.get('username', 'Користувач')

        if not telegram_id_str:
            return web.json_response({"error": "Missing telegram_id"}, status=400)

        telegram_id = int(telegram_id_str)


        await register_user(telegram_id=telegram_id, username=username)


        user_purchases = await get_user_purchases(telegram_id)

        if user_purchases is None:
            user_purchases = []

        return web.json_response({
            "telegram_id": telegram_id,
            "username": username,
            "purchases": user_purchases
        })
    except Exception as ex:
        print(f"Помилка в handle_get_profile: {ex}")
        return web.json_response({"error": str(ex)}, status=500)


def make_app():
    app = web.Application()

    app.router.add_get('/', handle_index)
    app.router.add_get('/api/products', handle_get_products)
    app.router.add_get('/api/profile', handle_get_profile)


    app.router.add_static('/pages/', path='pages', name='static')

    return app


if __name__ == '__main__':
    app = make_app()
    print("Асинхронний сервер запущено на http://localhost:8000")
    web.run_app(app, host='localhost', port=8000)