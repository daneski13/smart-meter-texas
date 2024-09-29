"""Example to show how to get 15 minute interval data for a meter."""

import asyncio
import logging
import os
import sys

import aiohttp
import pytz

import pandas as pd
import datetime

from smart_meter_texas import Account, Client, ClientSSLContext

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

username = os.environ["SMTUSER"]
password = os.environ["SMTPW"]

start_date = datetime.datetime(2024, 9, 1)
end_date = datetime.datetime(2024, 9, 27)

timezone = pytz.timezone("America/Chicago")


async def main():
    client_ssl_ctx = ClientSSLContext()
    ssl_context = await client_ssl_ctx.get_ssl_context()

    async with aiohttp.ClientSession() as websession:
        account = Account(username, password)
        client = Client(websession, account, ssl_context)

        print("Authenticating...")
        await client.authenticate()

        meters = await account.fetch_meters(client)

        for meter in meters:
            print("Reading meter...")
            await meter.get_interval(client, start_date, end_date)
            print(meter.read_interval.head(5))
            print(meter.read_interval.tail(5))

            # Get total consumption for the interval
            usage, start, end = meter.read_interval_consumption
            print(f"Consumption was {usage} kWh from {start} to {end}")

            # Get the total surplus generation for the interval
            surplus, start, end = meter.read_interval_surplus
            print(f"Surplus Generation was {surplus} kWh from {start} to {end}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
