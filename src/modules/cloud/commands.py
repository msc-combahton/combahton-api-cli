import logging
import json
import ipaddress
from configparser import ConfigParser
import click
from tabulate import tabulate
from tools.api import ApiRequest  # pylint: disable=import-error

cfgfile = ConfigParser()
cfgfile.read("config.ini")

logging.basicConfig(
    level=logging.getLevelName(cfgfile.get("core", "verbose"))
    if cfgfile.has_option("core", "verbose")
    else logging.INFO
)
logger = logging.getLogger(__name__)


api = ApiRequest()


@click.group()
def cloud():
    """cloud server management module"""


# region cloud
@click.command()
@click.argument("contract", type=click.INT)
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def view(contract, raw):
    request = api.request(component="kvm", method="server", action="view", id=contract)
    response = json.loads(request.text)
    if raw:
        click.echo(response)
    else:
        if response and response["status"] == "id_unauthenticated":
            logger.error("Access denied: You are not allowed to modify %s", contract)
        else:
            res = []
            for key, val in response.items():
                res.append([key, val])
            click.echo(tabulate(res))


@click.command()
@click.argument("contract", type=click.INT)
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def stop(contract, raw):
    request = api.request(
        component="kvm", method="server", action="control", id=contract, command="stop"
    )
    response = json.loads(request.text)
    if raw:
        click.echo(response)
    else:
        if (
            response
            and "status" in response
            and response["status"] == "id_unauthenticated"
        ):
            logger.error("Access denied: You are not allowed to modify %s", contract)
        elif response and "success" in response:
            if response["success"]:
                logger.info("Task OK")
            else:
                logger.error("Failed to stop the server: %s", response["success"])


@click.command()
@click.argument("contract", type=click.INT)
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def start(contract, raw):
    request = api.request(
        component="kvm", method="server", action="control", id=contract, command="start"
    )
    response = json.loads(request.text)
    if raw:
        click.echo(response)
    else:
        if (
            response
            and "status" in response
            and response["status"] == "id_unauthenticated"
        ):
            logger.error("Access denied: You are not allowed to modify %s", contract)
        elif response and "success" in response:
            if response["success"]:
                logger.info("Task OK")
            else:
                logger.error("Failed to start the server: %s", response["success"])


@click.command()
@click.argument("contract", type=click.INT)
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def reset(contract, raw):
    request = api.request(
        component="kvm", method="server", action="control", id=contract, command="reset"
    )
    response = json.loads(request.text)
    if raw:
        click.echo(response)
    else:
        if (
            response
            and "status" in response
            and response["status"] == "id_unauthenticated"
        ):
            logger.error("Access denied: You are not allowed to modify %s", contract)
        elif response and "success" in response:
            if response["success"]:
                logger.info("Task OK")
            else:
                logger.error(
                    "Failed to reset the server. Please ensure that the server is running before issuing a reset."
                )


@click.command()
@click.argument("contract", type=click.INT)
@click.argument("clientip")
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def vnc(contract, clientip, raw):
    try:
        ipaddr = str(ipaddress.ip_address(clientip))
    except ValueError:
        logger.error("client address/netmask is invalid: %s", clientip)
    except:
        logger.error("Usage: cloud vnc 610123 123.123.123.123")
        raise

    request = api.request(
        component="kvm",
        method="server",
        action="control",
        id=contract,
        command="vnc",
        source=ipaddr,
    )
    response = json.loads(request.text)
    if raw:
        click.echo(json.dumps(response))
    else:
        if (
            response
            and "status" in response
            and response["status"] == "id_unauthenticated"
        ):
            logger.error("Access denied: You are not allowed to modify %s", contract)
        else:
            res = []
            for key, val in response.items():
                res.append([key, val])
            click.echo(tabulate(res))


# endregion


# region reinstall
@click.group()
def reinstall():
    """cloud server reinstall module"""


@click.command()
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def list_templates(raw):
    request = api.request(
        component="kvm", method="server", action="reinstall_templates"
    )
    response = json.loads(request.text)
    if raw:
        click.echo(response)
    else:
        click.echo(tabulate(response, headers="keys"))


@click.command()
@click.argument("contract", type=click.INT)
@click.argument("template-id", type=click.INT)
@click.option("-r", "--raw", is_flag=True, help="Return the raw JSON response")
def run(contract, template_id, raw):
    request = api.request(
        component="kvm",
        method="server",
        action="reinstall",
        id=contract,
        template=template_id,
    )
    response = json.loads(request.text)
    if raw:
        click.echo(response)
    else:
        if response and "status" in response:
            if response["status"] == "id_unauthenticated":
                logger.error(
                    "Access denied: You are not allowed to modify %s", contract
                )
            elif response["status"] == "id_reinstalling":
                logger.error(
                    "Access denied: A reinstallation is already running for %s",
                    contract,
                )
            elif response["status"] == "OK":
                logger.info("Task OK: Reinstallation started")


# endregion
cloud.add_command(view)
cloud.add_command(stop)
cloud.add_command(start)
cloud.add_command(reset)
cloud.add_command(vnc)
cloud.add_command(reinstall)

reinstall.add_command(list_templates)
reinstall.add_command(run)
