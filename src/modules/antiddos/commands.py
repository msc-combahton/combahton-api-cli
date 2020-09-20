import click
import json
import ipaddress
import sys

import logging
logger = logging.getLogger(__name__)

from tools.api import ApiRequest
from tabulate import tabulate

api = ApiRequest()

@click.group()
def antiddos():
    """antiddos management module"""
    pass


@click.command()
@click.argument('ipv4')
@click.argument('toggle', type=click.BOOL)
def fv3(ipv4, toggle):
    """Enable/Disable flowShield v3 on the specified IPv4 address - toggle is of type boolean"""
    try:
        ipaddr = str(ipaddress.ip_address(ipv4))
        request = api.request(component = "antiddos", method = "layer4", action = "routing", routing = "l4_target", target = ('fv3' if toggle else 'fv3'), ipaddr = ipaddr)
        response = json.loads(request.text)
        if response and response["status"]  == 'routing_changed':
            click.echo("OK")
            logger.info("Response: %s" % response)
        elif response and response["status"] == "id_unauthenticated":
            click.echo("Access denied: You are not allowed to modify %s" % ipaddr)
            logger.info("Response: %s" % response)
        else:
            logger.error(response["status"])
    except ValueError:
        logger.error("address/netmask is invalid: %s "  % click.get_os_args()[2])
    except:
        logger.error('Usage: antiddos fv3 127.0.0.1 true')
        raise

@click.command()
@click.argument('ipv4')
@click.argument('type')
def l4_routing(ipv4, type):
    """Set the Layer 4 routing mode of the specified IPv4 - valid types are dynamic, permanent, dynamic_perm"""
    try:
        ipaddr = str(ipaddress.ip_address(ipv4))
        request = api.request(component = "antiddos", method = "layer4", action = "routing", routing = type, ipaddr = ipaddr)
        response = json.loads(request.text)
        if response and response["status"]  == 'routing_changed':
            logger.info(response)
            click.echo("OK")
        else:
            logger.error(response["status"])
    except ValueError:
        logger.error("address/netmask is invalid: %s "  % click.get_os_args()[2])
    except:
        logger.error('Usage: antiddos l4-routing 127.0.0.1 true')
        raise


@click.command()
@click.argument('ipv4')
@click.argument('type')
def l7_routing(ipv4, type):
    """Set the Layer 7 routing mode of the specified IPv4 - valid types are only_on, only_off, activate, deactivate"""
    try:
        ipaddr = str(ipaddress.ip_address(ipv4))
        request = api.request(component = "antiddos", method = "layer7", action = "routing", routing = type, ipaddr = ipaddr)
        response = json.loads(request.text)
        if response and response["status"]  == 'routing_changed':
            logger.info(response)
            click.echo("OK")
        else:
            logger.error(response["status"])
    except ValueError:
        logger.error("address/netmask is invalid: %s "  % click.get_os_args()[2])
    except:
        logger.error('Usage: antiddos l7-routing 127.0.0.1 true')
        raise

@click.command()
@click.argument('ipv4')
@click.option('-r', '--raw', is_flag = True, help = "Return the raw JSON response")
def incidents_single(ipv4, raw):
    """Shows the last 25 ddos incidents for a specific ip"""
    try:
        ipaddr = str(ipaddress.ip_address(ipv4))
        request = api.request(component = "antiddos", method = "incidents", action = "show", ipaddr = ipaddr)
        response = json.loads(request.text)
        if raw:
            click.echo(response)
        else:
            click.echo(tabulate(response,headers="keys"))
    except ValueError:
        logger.error("address/netmask is invalid: %s "  % click.get_os_args()[2])
    except:
        logger.error('Usage: antiddos incidents-ip 127.0.0.1')
        raise

@click.command()
@click.option('-r', '--raw', is_flag = True, help = "Return the raw JSON response")
def incidents_all(raw):
    """Shows the last 100 incidents in total"""
    try:
        request = api.request(component = "antiddos", method = "incidents", action = "show_all")
        response = json.loads(request.text)
        if raw:
            click.echo(response)
        else:
            click.echo(tabulate(response,headers="keys"))
    except:
        logger.error('Usage: antiddos incident-all 127.0.0.1')
        raise

@click.command()
@click.argument('ipv4')
@click.option('-r', '--raw', is_flag = True, help = "Return the raw JSON response")
def status(ipv4, raw):
    """Shows the current status of a specific ip"""
    try:
        ipaddr = str(ipaddress.ip_address(ipv4))
        request = api.request(component = "antiddos", method = "status", action = "show", ipaddr = ipaddr)
        response = json.loads(request.text)
        if raw:
            click.echo(response)
        else:
            click.echo(tabulate(response,headers="keys"))
    except ValueError:
        logger.error("address/netmask is invalid: %s "  % click.get_os_args()[2])
    except:
        logger.error('Usage: antiddos incidents-ip 127.0.0.1')
        raise

antiddos.add_command(fv3)
antiddos.add_command(l4_routing)
antiddos.add_command(l7_routing)
antiddos.add_command(incidents_single)
antiddos.add_command(incidents_all)
antiddos.add_command(status)