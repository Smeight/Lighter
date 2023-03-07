import unittest
import asyncio
import aiohttp
import json


class TestFlashlight(unittest.TestCase):

    async def test_on_command(self):
        async with aiohttp.ClientSession() as session:
            url = 'http://localhost:8080/command'
            data = {'command': 'ON'}
            async with session.post(url, json=data) as resp:
                self.assertEqual(resp.status, 200)
                result = await resp.json()
                self.assertEqual(result['status'], 'success')

    async def test_off_command(self):
        async with aiohttp.ClientSession() as session:
            url = 'http://localhost:8080/command'
            data = {'command': 'OFF'}
            async with session.post(url, json=data) as resp:
                self.assertEqual(resp.status, 200)
                result = await resp.json()
                self.assertEqual(result['status'], 'success')

    async def test_color_command(self):
        async with aiohttp.ClientSession() as session:
            url = 'http://localhost:8080/command'
            data = {'command': 'COLOR', 'metadata': 'blue'}
            async with session.post(url, json=data) as resp:
                self.assertEqual(resp.status, 200)
                result = await resp.json()
                self.assertEqual(result['status'], 'success')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        TestFlashlight().test_on_command(),
        TestFlashlight().test_off_command(),
        TestFlashlight().test_color_command()
    ))
    loop.close()
