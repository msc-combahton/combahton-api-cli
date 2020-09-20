import click
import json
from tools.api import ApiRequest

def confirmCallback(ctx, param, value):
    if not value:
        ctx.abort()

@click.group()
def customer():
    """customer management module"""
    pass

@click.command()
def invoice_all():
    api = ApiRequest()
    request = api.request(component = "customer", method = "invoices", action = "view_all") 
    invoices = json.loads(request.text)
    print(invoices)

@click.command()
def invoice_unpaid():
    api = ApiRequest()
    request = api.request(component = "customer", method = "invoices", action = "view_unpaid") 
    invoices = json.loads(request.text)
    if invoices["status"] == 'invoices_paid':
        click.echo("You have no unpaid invoices.")
    else:
        click.echo(invoices)

@click.command()
@click.argument('id')
def invoice(id):
    api = ApiRequest()
    request = api.request(component = "customer", method = "invoices", action = "view", id = id)
    print(request.text)
    """with open(("%s.pdf" % id), "w") as fileHandle:
        fileHandle.write(request.text)
        click.echo("Invoice saved as %s.pdf" % id)"""

@click.command()
@click.option('-c', is_flag=True, default = False)
@click.option('--currency', is_flag=True, default = False)
def credits(c, currency):
    api = ApiRequest()
    request = api.request(component = "customer", method = "credits", action = "view") 
    credit = json.loads(request.text)
    if credit:
        click.echo("%s %s" % (credit['amount'], ("EUR" if currency or c else "")))
    else:
        click.echo(request.text)

@click.command()
def contract_all():
    api = ApiRequest()
    request = api.request(component = "customer", method = "contract", action = "view_all")
    contracts = json.loads(request.text)
    if contracts:
        click.echo(contracts)
    else:
        click.echo(request.text)

@click.command()
@click.argument('id')
def contract(id):
    api = ApiRequest()
    request = api.request(component = "customer", method = "contract", action = "view", id = id)
    contracts = json.loads(request.text)
    if contracts:
        click.echo(contracts)
    else:
        click.echo(request.text)

@click.command()
@click.argument('id')
def contract_extend(id):
    api = ApiRequest()
    request = api.request(component = "customer", method = "contract", action = "extend", id = id)
    contracts = json.loads(request.text)
    if contracts:
        click.echo(contracts)
    else:
        click.echo(request.text)

@click.command()
@click.argument('id')
@click.option('--enable', is_flag=True, default=False)
def contract_autoextend(id, enable):
    """Modifies auto-extension for the given contract.
    Default action is disabling auto-extend.
    To enable, pass --enable"""
    switch = ("enable" if enable else "disable")
    api = ApiRequest()
    request = api.request(component = "customer", method = "contract", action = "autoextend", id = id, switch = switch)
    contracts = json.loads(request.text)
    if contracts:
        click.echo(contracts)
    else:
        click.echo(request.text)

@click.command()
@click.argument('product')
@click.option('--yes', is_flag=True, callback=confirmCallback, expose_value=False, prompt="Are you sure?")
def contract_order(product):
    """Orders a specific product"""
    api = ApiRequest()
    request = api.request(component = "customer", method = "contract", action = "order", id = product)
    contracts = json.loads(request.text)
    if contracts:
        click.echo(contracts)
    else:
        click.echo(request.text)

customer.add_command(invoice_all)
customer.add_command(invoice_unpaid)
customer.add_command(invoice)
customer.add_command(credits)
customer.add_command(contract)
customer.add_command(contract_all)
customer.add_command(contract_extend)
customer.add_command(contract_autoextend)
customer.add_command(contract_order)