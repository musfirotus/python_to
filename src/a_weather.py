import asyncio # install
import click # install
import json
import time
from datetime import datetime # install
from functools import wraps
from src.Fetch import Fetcher as fetcher

def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper

@click.group()
async def cli():
    pass

@cli.command(name="weather")
@click.argument("city",type=click.STRING)
@click.option("--celcius",is_flag=True,default=False,type=click.BOOL)
@click.option("--fahrenheit",is_flag=True,default=False,type=click.BOOL)
@click.option("--kelvin",is_flag=True,default=False,type=click.BOOL)
@click.option("--temp",is_flag=True,default=False,type=click.BOOL)
@coro
async def weather(city,celcius,fahrenheit,temp,kelvin):
    start = time.time()
    tempss = "metric" if celcius else "imperial" if fahrenheit else None
    word = "Celcius" if celcius else "Fahrenheit" if fahrenheit else "Kelvin"
    temps = tempss if tempss else None
    print(f"started at {time.strftime('%X')}")
    datas = await fetcher.get(f'http://api.openweathermap.org/data/2.5/weather?q={city.lower()}&units={temps}&appid=b778b00e0b799500ac184f565004d718')
    data = json.loads(datas)
    # print(data)
    dates = datetime.fromtimestamp(1599712037).strftime("%A, %B %d, %Y %H:%M:%S %p")
    sunrises = datetime.fromtimestamp(data['sys']['sunrise']).strftime("%A, %B %d, %Y %H:%M:%S %p")
    sunsets = datetime.fromtimestamp(data['sys']['sunset']).strftime("%A, %B %d, %Y %H:%M:%S %p")
    if data['cod'] != '404':
        if (temp and (celcius or fahrenheit or kelvin)) or temp:
            print(dates)
            print('-' * len(dates))
            print(f"{data['main']['temp']} {word} | {data['clouds']['all']}")
        else:
            if celcius or fahrenheit or kelvin:
                results = []
                results.append(f"datetime\t: {dates}")
                results.append(f"city\t\t: {data['name']}")
                results.append(f"temperature\t: {data['main']['temp']} {word}")
                results.append(f"weather\t\t: {data['clouds']['all']}")
                results.append(f"sunrise\t\t: {sunrises}")
                results.append(f"sunset\t\t: {sunsets}")
                print("\n".join(results))
    else:
        print("ERROR!")
    end = time.time()
    print(f"Finished at {time.strftime('%X')}")
    print(f"Total time: {round(int(end - start))}")

if __name__ == "__main__":
    cli()