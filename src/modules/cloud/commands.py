import click

import logging

logger = logging.getLogger(__name__)

@click.group()
def cloud():
    """cloud server management module"""
    pass

@click.command()
def test():
    logger.info("kekw")

cloud.add_command(test)