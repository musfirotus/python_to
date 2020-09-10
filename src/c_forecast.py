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

@cli.command(name="forecast")
@click.argument("city",type=click.STRING)
@click.option("--days",is_flag=True,default=False,type=click.BOOL)
@coro
async def forecast(city,days):
    start = time.time()
    print(f"started at {time.strftime('%X')}")
    datas = await fetcher.get(f'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid=b778b00e0b799500ac184f565004d718')
    data = json.loads(datas)
    dates = datetime.fromtimestamp(1599712037).strftime("%A, %B %d, %Y %H:%M:%S %p")
    # print(data)
    if data['cod'] != '404':
        print(dates)
        print('-' * 50)
        def data3(data):
            return datetime.utcfromtimestamp(data).strftime('%Y %m %d') == datetime.now().strftime('%Y %m %d')
        data = list(x for x in data['list'] if data3(x['dt']))
        for d in data:
            main = " ".join(list(d['main'] + ', ' +d['description'] for d in d['weather']))
            print(f'{datetime.fromtimestamp(d["dt"]).strftime("%I:%M %p")} | {d["main"]["temp"]}° Celcius | {main}')
    else:
        print("ERROR!")
    end = time.time()
    print(f"Finished at {time.strftime('%X')}")
    print(f"Total time: {round(int(end - start))}")

if __name__ == "__main__":
    cli()