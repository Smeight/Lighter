import asyncio
import json

from aiohttp import web


async def websocket_handler(request):
    """
    Обработчик WebSocket-соединений
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    while True:
        try:
            # Читаем сообщение от клиента
            message = await ws.receive()

            # Если сообщение от клиента является текстовым
            if message.type == web.WSMsgType.text:
                try:
                    # Разбираем сообщение как JSON
                    data = json.loads(message.data)
                    command = data.get('command')
                    metadata = data.get('metadata')
                    if command == 'ON':
                        print('Turning on the light')
                        # Отправляем сообщение о включении фонаря
                        await ws.send_json({'status': 'success', 'message': 'The light is on'})
                    elif command == 'OFF':
                        print('Turning off the light')
                        # Отправляем сообщение о выключении фонаря
                        await ws.send_json({'status': 'success', 'message': 'The light is off'})
                    elif command == 'COLOR':
                        color = metadata.get('color')
                        print(f'Changing the color to {color}')
                        # Отправляем сообщение об изменении цвета фонаря
                        await ws.send_json({'status': 'success', 'message': f'The color is changed to {color}'})
                    else:
                        # Отправляем сообщение об ошибке - неизвестная команда
                        await ws.send_json({'status': 'error', 'message': f'Unknown command: {command}'})
                except Exception as e:
                    # Отправляем сообщение об ошибке - некорректный JSON
                    await ws.send_json({'status': 'error', 'message': f'Invalid JSON data: {e}'})
            # Если сообщение от клиента является бинарным
            elif message.type == web.WSMsgType.binary:
                # Отправляем сообщение об ошибке - бинарные данные не поддерживаются
                await ws.send_json({'status': 'error', 'message': 'Binary data is not supported'})
            # Если клиент закрыл соединение
            elif message.type == web.WSMsgType.closed:
                print('Connection closed by client')
                break
        except Exception as e:
            print(f'Error handling message: {e}')
            break

    return ws


async def main():
    app = web.Application()
    app.add_routes([web.get('/', websocket_handler)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 8080)
    await site.start()

    while True:
        await asyncio.sleep(3600)  # ждем один час


if __name__ == '__main__':
    asyncio.run(main())

