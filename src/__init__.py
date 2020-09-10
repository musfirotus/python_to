import click
from src.a_weather import weather
from src.c_forecast import forecast

@click.group()
def cli():
    pass

cli.add_command(weather)
cli.add_command(forecast)

if __name__ == '__main__':
    cli()