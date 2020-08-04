import click
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

@click.command()
@click.argument('email')
@click.argument('key')
def cli(email, key):
    """login module"""
    with open("config.ini", "w") as f:
        if not config.has_section('api'):
            config.add_section('api')
        config.set('api', 'email', email)
        config.set('api', 'key', key)
        config.write(f)
    click.echo("Saved credentials for %s" % email)