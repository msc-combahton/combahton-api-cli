import logging
import json
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


def confirm_callback(ctx, param, value):
    if not param or not value:
        ctx.abort()


@click.group()
def customer():
    """customer management module"""


@click.command()
def invoice_all():
    api = ApiRequest()
    request = api.request(component="customer", method="invoices", action="view_all")
    invoices = json.loads(request.text)
    print(invoices)


@click.command()
def invoice_unpaid():
    api = ApiRequest()
    request = api.request(component="customer", method="invoices", action="view_unpaid")
    invoices = json.loads(request.text)
    if invoices["status"] == "invoices_paid":
        click.echo("You have no unpaid invoices.")
    else:
        click.echo(invoices)


@click.command()
@click.option("-c", "--currency", is_flag=True, default=False)
def credit(currency):
    api = ApiRequest()
    request = api.request(component="customer", method="credits", action="view")
    user_credits = json.loads(request.text)
    if user_credits:
        click.echo("%s %s" % (user_credits["amount"], ("EUR" if currency else "")))
    else:
        click.echo(request.text)


@click.command()
def contract_all():
    api = ApiRequest()
    request = api.request(component="customer", method="contract", action="view_all")
    contracts = json.loads(request.text)
    if contracts:
        click.echo(tabulate(contracts, headers="keys"))
    else:
        logger.error(request.text)


@click.command()
@click.argument("contract_id")
def contract(contract_id):
    api = ApiRequest()
    request = api.request(
        component="customer", method="contract", action="view", id=contract_id
    )
    contracts = json.loads(request.text)
    if contracts:
        res = []
        for key, val in contracts.items():
            res.append([key, val])
        click.echo(tabulate(res))
    else:
        logger.error(request.text)


@click.command()
@click.argument("contract_id")
def contract_extend(contract_id):
    api = ApiRequest()
    request = api.request(
        component="customer", method="contract", action="extend", id=contract_id
    )
    response = json.loads(request.text)
    if response and "status" in response:
        if response["status"] == "extended":
            logger.info("Contract %s extended", contract_id)
        elif response["status"] == "id_unauthenticated":
            logger.error("Access denied: You are not allowed to modify %s", contract_id)
        else:
            logger.error(response["status"])
    else:
        click.echo(request.text)


@click.command()
@click.argument("contract_id")
@click.argument("toggle", type=click.BOOL)
def contract_autoextend(contract_id, toggle):
    """Modifies auto-extension for the given contract."""
    switch = "enable" if toggle else "disable"
    api = ApiRequest()
    request = api.request(
        component="customer",
        method="contract",
        action="autoextend",
        id=contract_id,
        switch=switch,
    )
    response = json.loads(request.text)
    if response and "status" in response:
        if response["status"] == "autoextend_disabled":
            logger.info("autoextend has been disabled for %s", contract_id)
        elif response["status"] == "autoextend_enabled":
            logger.info("autoextend has been enabled for %s", contract_id)
        elif response["status"] == "id_unauthenticated":
            logger.error(
                "Access denied: You are not allowed to modify contract %s", contract_id
            )
        else:
            logger.error(response["status"])
    else:
        click.echo(request.text)


@click.command()
@click.argument("product")
@click.option(
    "--yes",
    is_flag=True,
    callback=confirm_callback,
    expose_value=False,
    prompt="Are you sure?",
)
def contract_order(product):
    """Orders a specific product"""
    api = ApiRequest()
    request = api.request(
        component="customer", method="contract", action="order", id=product
    )
    response = json.loads(request.text)
    if response and "status" in response:
        if response["status"] == "order_placed":
            logger.info("Your order has been placed as %s", response["id"])
        else:
            logger.error(response["status"])
    else:
        click.echo(request.text)


customer.add_command(invoice_all)
customer.add_command(invoice_unpaid)
customer.add_command(credit)
customer.add_command(contract)
customer.add_command(contract_all)
customer.add_command(contract_extend)
customer.add_command(contract_autoextend)
customer.add_command(contract_order)
