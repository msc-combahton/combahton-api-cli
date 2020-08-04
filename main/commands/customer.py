import click
import json
from api.request import ApiRequest

@click.group()
def cli():
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
    click.echo("Showing unpaid invoices.")

@click.command()
@click.argument('id')
def invoice(id):
    api = ApiRequest()
    api.request(component = "customer", method = "invoices", action = "view", id = id) 

cli.add_command(invoice_all)
cli.add_command(invoice_unpaid)
cli.add_command(invoice)