import click
import json
import ipaddress
import sys

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

from tools.api import ApiRequest # pylint: disable=import-error
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
    """Manage flowShieldv3 on a specified IPv4 address"""
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
    """Set the Layer 4 routing mode of the specified IPv4
    
    Valid types are dynamic, permanent, dynamic_perm"""
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
    """Set the Layer 7 routing mode of the specified IPv4
    
    Valid types are only_on, only_off, activate, deactivate"""
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
    """Shows the current filter status of a specific ip"""
    try:
        ipaddr = str(ipaddress.ip_address(ipv4))
        request = api.request(component = "antiddos", method = "status", action = "show", ipaddr = ipaddr)
        response = json.loads(request.text)
        if response and 'status' in response:
            if response['status'] == 'id_unauthenticated':
                logger.error("Access denied: You are not allowed to modify %s" % ipaddr)
        else:
            if raw:
                click.echo(response)
            else:
                res = []  
                for key,val in response.items():
                    res.append([key, val])
                click.echo(tabulate(res))
    except ValueError:
        logger.error("address/netmask is invalid: %s "  % click.get_os_args()[2])
        raise
    except:
        logger.error('Usage: antiddos status 127.0.0.1')
        raise

@click.command()
@click.argument('domain')
@click.argument('protection', default="")
@click.option('-r', '--raw', is_flag = True, help = "Return the raw JSON response")
def l7_domain_add(domain, protection, raw):
    """Adds the DOMAIN to the layer7 filtering, optionally setting the PROTECTION.
    
    DOMAIN is a FQDN whose A-Record points o an IPv4-address owned by your account.
    PROTECTION is a method like aes, captcha, button
    """
    try:
        request = api.request(component = "antiddos", method = "layer7", action = "add", domain = domain, protector=protection)
        response = json.loads(request.text)
        if response and 'status' in response:
            if response['status'] == 'id_unauthenticated':
                logger.error("Access denied: You are not allowed to modify %s" % domain)
        else:
            if raw:
                click.echo(response)
            else:
                res = []  
                for key,val in response.items():
                    res.append([key, val])
                click.echo(tabulate(res))
    except ValueError:
        logger.error("address/netmask is invalid: %s "  % click.get_os_args()[2])
        raise
    except:
        logger.error('Usage: antiddos status 127.0.0.1')
        raise

@click.group()
def layer7():
    """Layer 7 API methods"""
    pass

@click.group()
def layer4():
    """Layer 4 API methods"""
    pass

@click.group()
def incidents():
    """Incident Methods"""
    pass


antiddos.add_command(fv3)
antiddos.add_command(status)

"""Layer 4 Submodule"""
layer4.add_command(l4_routing, name = "set-routing")

"""Layer 7 Submodule"""
layer7.add_command(l7_routing, name = "set-routing")
layer7.add_command(l7_domain_add, name="domain-add")

"""Incident Submodule"""
incidents.add_command(incidents_single, name="single")
incidents.add_command(incidents_all, name="all")

antiddos.add_command(layer4)
antiddos.add_command(layer7)
antiddos.add_command(incidents)