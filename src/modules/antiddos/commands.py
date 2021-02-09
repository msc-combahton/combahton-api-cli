import logging
import json
import ipaddress
from configparser import ConfigParser
import click
from tabulate import tabulate
from tools.api import ApiRequest  # pylint: disable=import-error
from tools.config import cfgfile  # pylint: disable=import-error

logging.basicConfig(
    level=logging.getLevelName(cfgfile.get("core", "verbose"))
    if cfgfile.has_option("core", "verbose")
    else logging.INFO
)
logger = logging.getLogger(__name__)

api = ApiRequest()


@click.group()
def antiddos():
    """antiddos management module"""


# region General
@click.command()
@click.argument("ipv4")
@click.argument("toggle", type=click.BOOL)
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def fv3(ipv4, toggle, raw):
    """[DEPRECATED] Manage flowShieldv3 on a specified IPv4 address"""
    # pylint: disable=unused-argument
    logger.warning(
        "This command is deprecated as flowShieldv3 is already rolled out as default. No changes have been applied to the infrastructure."
    )
    logger.info("Routing changed")


@click.command()
@click.argument("ipv4")
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def status(ipv4, raw):
    """Shows the current filter status of a specific ip"""
    try:
        ipaddr = str(ipaddress.ip_address(ipv4))
        request = api.request(
            component="antiddos", method="status", action="show", ipaddr=ipaddr
        )
        response = json.loads(request.text)
        if response and "status" in response:
            if response["status"] == "id_unauthenticated":
                logger.error("Access denied: You are not allowed to modify %s", ipaddr)
        else:
            if raw:
                click.echo(request.text)
            else:
                res = []
                for key, val in response.items():
                    res.append([key, val])
                click.echo(tabulate(res))
    except ValueError:
        logger.error("address/netmask is invalid: %s ", click.get_os_args()[2])
        raise
    except:
        logger.error("Usage: antiddos status 127.0.0.1")
        raise


# endregion

# region Layer 4
@click.group()
def layer4():
    """Layer 4 API methods"""


@click.command()
@click.argument("ipv4")
@click.argument("routing_type")
def l4_routing(ipv4, routing_type):
    """Set the Layer 4 routing mode of the specified IPv4

    Valid types are dynamic, permanent, dynamic_perm"""
    try:
        ipaddr = str(ipaddress.ip_address(ipv4))
        request = api.request(
            component="antiddos",
            method="layer4",
            action="routing",
            routing=routing_type,
            ipaddr=ipaddr,
        )
        response = json.loads(request.text)
        if response and response["status"] == "routing_changed":
            logger.info(response)
            click.echo("OK")
        else:
            logger.error(response["status"])
    except ValueError:
        logger.error("address/netmask is invalid: %s ", click.get_os_args()[2])
    except:
        logger.error("Usage: antiddos l4-routing 127.0.0.1 true")
        raise


# endregion

# region Layer 7
@click.group()
def layer7():
    """Layer 7 API methods"""


@click.command()
@click.argument("ipv4")
@click.argument("routing_type")
def l7_routing(ipv4, routing_type):
    """Set the Layer 7 routing mode of the specified IPv4

    Valid types are only_on, only_off, activate, deactivate"""
    try:
        ipaddr = str(ipaddress.ip_address(ipv4))
        request = api.request(
            component="antiddos",
            method="layer7",
            action="routing",
            routing=routing_type,
            ipaddr=ipaddr,
        )
        response = json.loads(request.text)
        if response and response["status"] == "routing_changed":
            logger.info(response)
            click.echo("OK")
        else:
            logger.error(response["status"])
    except ValueError:
        logger.error("address/netmask is invalid: %s ", click.get_os_args()[2])
    except:
        logger.error("Usage: antiddos l7-routing 127.0.0.1 true")
        raise


@click.command()
@click.argument("domain")
@click.argument("protection", default="buttom")
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def l7_domain_add(domain, protection, raw):
    """Adds the DOMAIN to the layer7 filtering, optionally setting the PROTECTION.

    DOMAIN is a FQDN whose A-Record points o an IPv4-address owned by your account.
    PROTECTION is a method like aes, captcha, button
    """
    try:
        request = api.request(
            component="antiddos",
            method="layer7",
            action="add",
            domain=domain,
            protector=protection,
        )
        response = json.loads(request.text)
        if raw:
            click.echo(request.text)
        elif response and "status" in response:
            if response["status"] == "id_unauthenticated":
                logger.error("Access denied: You are not allowed to modify %s", domain)
            elif response["status"] == "added":
                logger.error("Domain %s has been added", domain)
            elif response["status"] == "exists":
                logger.error("Domain %s already exists", domain)
            else:
                logger.debug(response["status"])
        else:
            logger.error("An unknown error occured. Please try again later.")
    except:
        logger.error("Usage: antiddos layer7 domain-add example.tld [protector]")
        raise


@click.command()
@click.argument("domain")
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def l7_domain_delete(domain, raw):
    """Removes DOMAIN from the layer7 filtering"""
    try:
        request = api.request(
            component="antiddos", method="layer7", action="delete", domain=domain
        )
        response = json.loads(request.text)
        if raw:
            click.echo(request.text)
        elif response and "status" in response:
            if response["status"] == "id_unauthenticated":
                logger.error("Access denied: You are not allowed to modify %s", domain)
            elif response["status"] == "deleted":
                logger.error("Domain %s has been removed", domain)
            else:
                logger.debug(response["status"])
        else:
            logger.error("An unknown error occured. Please try again later.")
    except:
        logger.error("Usage: antiddos layer7 domain-remove example.tld")
        raise


@click.command()
@click.argument("domain")
@click.argument("certificate", type=click.Path("r"))
@click.argument("privatekey", type=click.Path("r"))
@click.argument("protection", default="button")
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def l7_ssl_add(domain, certificate, privatekey, protection, raw):
    """Adds an SSL secured DOMAIN from the layer7 filtering

    Example: antiddos layer7 ssl-add example.tld /path/to/certificate /path/to/keyfile
    """
    try:
        with open(certificate) as cert:
            with open(privatekey) as priv:
                request = api.request(
                    component="antiddos",
                    method="layer7",
                    action="ssl_add",
                    domain=domain,
                    cert=cert.read(),
                    key=priv.read(),
                    protector=protection,
                )
                response = json.loads(request.text)
                if raw:
                    click.echo(request.text)
                elif response and "status" in response:
                    if response["status"] == "id_unauthenticated":
                        logger.info(response)
                        logger.error(
                            "Access denied: You are not allowed to modify %s", domain
                        )
                    elif response["status"] == "ssl_chain_invalid":
                        logger.error(
                            "The provided SSL chain is invalid. Please check your input."
                        )
                    elif response["status"] == "added":
                        logger.info("Successfully added %s", domain)
                    else:
                        logger.error(response["status"])
                else:
                    logger.error("An unknown error occured. Please try again later.")
    except:
        logger.error(
            "Usage: antiddos layer7 ssl-add example.tld /path/to/certificate /path/to/keyfile [protection]"
        )
        raise


@click.command()
@click.argument("domain")
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def l7_ssl_remove(domain, raw):
    """Removes ssl secured DOMAIN from the layer7 filtering"""
    try:
        request = api.request(
            component="antiddos", method="layer7", action="ssl_delete", domain=domain
        )
        response = json.loads(request.text)
        if raw:
            click.echo(request.text)
        elif response and "status" in response:
            if response["status"] == "id_unauthenticated":
                logger.error("Access denied: You are not allowed to modify %s", domain)
            elif response["status"] == "deleted":
                logger.error("Domain %s has been removed", domain)
            else:
                logger.debug(response["status"])
        else:
            logger.error("An unknown error occured. Please try again later.")
    except:
        logger.error("Usage: antiddos layer7 ssl-remove example.tld")
        raise


@click.command()
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def l7_ssl_view(raw):
    """Shows all SSL certificates known to the filter"""
    try:
        request = api.request(component="antiddos", method="layer7", action="ssl_view")
        response = json.loads(request.text)
        if response and "status" in response:
            logger.debug(response["status"])
        else:
            if raw:
                click.echo(request.text)
            else:
                click.echo(tabulate(response, headers="keys"))
    except:
        logger.error("Usage: antiddos layer7 ssl-remove example.tld")
        raise


# endregion

# region Incidents
@click.group()
def incidents():
    """Incident Methods"""


@click.command()
@click.argument("ipv4")
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def incidents_single(ipv4, raw):
    """Shows the last 25 ddos incidents for a specific ip"""
    try:
        ipaddr = str(ipaddress.ip_address(ipv4))
        request = api.request(
            component="antiddos", method="incidents", action="show", ipaddr=ipaddr
        )
        response = json.loads(request.text)
        if raw:
            click.echo(request.text)
        else:
            click.echo(tabulate(response, headers="keys"))
    except ValueError:
        logger.error("address/netmask is invalid: %s", ipv4)
    except:
        logger.error("Usage: antiddos incidents-ip 127.0.0.1")
        raise


@click.command()
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def incidents_all(raw):
    """Shows the last 100 incidents in total"""
    try:
        request = api.request(
            component="antiddos", method="incidents", action="show_all"
        )
        response = json.loads(request.text)
        if raw:
            click.echo(request.text)
        else:
            click.echo(tabulate(response, headers="keys"))
    except:
        logger.error("Usage: antiddos incident-all 127.0.0.1")
        raise


# endregion

antiddos.add_command(fv3)
antiddos.add_command(status)

# Layer 4 Submodule
layer4.add_command(l4_routing, name="set-routing")

# Layer 7 Submodule
layer7.add_command(l7_routing, name="set-routing")

layer7.add_command(l7_domain_add, name="domain-add")
layer7.add_command(l7_domain_delete, name="domain-remove")

layer7.add_command(l7_ssl_add, name="ssl-add")
layer7.add_command(l7_ssl_remove, name="ssl-remove")
layer7.add_command(l7_ssl_view, name="ssl-view")

# Incident Submodule
incidents.add_command(incidents_single, name="single")
incidents.add_command(incidents_all, name="all")

antiddos.add_command(layer4)
antiddos.add_command(layer7)
antiddos.add_command(incidents)
