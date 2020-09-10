import click
from src.a_weather import weather

@click.group()
def cli():
    pass

# Number 1
cli.add_command(weather)

if __name__ == '__main__':
    cli()