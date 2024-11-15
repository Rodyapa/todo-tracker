import os

from aiohttp import web, ClientSession

AIOHTTP_PORT = int(os.getenv('AIOHTTP_PORT'))
AIOHTTP_HOST = os.getenv('AIOHTTP_HOST')


async def proxy_handler(request):
    target_url = f"http://backend:8000{request.rel_url}"
    async with ClientSession() as session:
        async with session.request(
            request.method, target_url,
            headers=request.headers, data=await request.read()
        ) as resp:
            headers = {k: v for k, v in resp.headers.items()}
            return web.Response(
                status=resp.status, headers=headers, body=await resp.read()
            )

app = web.Application()
app.router.add_route('*', '/{path_info:.*}', proxy_handler)

if __name__ == '__main__':
    web.run_app(app, host=AIOHTTP_HOST, port=AIOHTTP_PORT)
