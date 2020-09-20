import click
import sys
import os

if getattr(sys, 'frozen', False):
    sys.tracebacklimit = 0

from configparser import ConfigParser
cfgfile = ConfigParser()
cfgfile.read('config.ini')

import logging
logger = logging.getLogger(__name__)

from modules.antiddos import commands as antiddos
from modules.cloud import commands as cloud
from modules.customer import commands as customer
from modules.config import commands as config

@click.group()
def cli():
    """Simple CLI Interface to interact with the combahton API"""
    if cfgfile.has_section("core"):
        if cfgfile.has_option("core","verbosity"):
            logger.setLevel(logging.getLevelName(cfgfile.get("core","verbosity")))
    pass


cli.add_command(antiddos.antiddos)
cli.add_command(config.config)
cli.add_command(customer.customer)
cli.add_command(cloud.cloud)

if __name__ == '__main__':
    cli()