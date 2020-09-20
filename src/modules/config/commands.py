import click
from configparser import ConfigParser

cfgfile = ConfigParser()
cfgfile.read('config.ini')

@click.group()
def config():
    """configuration module"""
    pass

@click.command()
@click.argument('index')
@click.argument('value')
def set(index, value):
    """Set parameters for config"""
    namespace, key = index.split('.', 1)
    with open("config.ini", "w") as f:
        if not cfgfile.has_section(namespace):
            cfgfile.add_section(namespace)
        cfgfile.set(namespace, key, value)
        cfgfile.write(f)

@click.command()
@click.argument('namespace')
def get(namespace):
    """Show namespace from config"""
    if not cfgfile.has_section(namespace):
        click.echo("Namespace not found.")
    else:
        for item in cfgfile.items(namespace):
            click.echo(namespace + "." + item[0] + ": " + item[1])

@click.command()
def clear():
    """Remove stored credentials from config.ini"""
    if cfgfile.has_section('api'):
        with open('config.ini', 'w') as f:
            f.write("")
    else:
        click.echo("There were no credentials stored.") 

config.add_command(set)
config.add_command(get)
config.add_command(clear)