import click
import sys
import os

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')
class CbCLI(click.MultiCommand):
    def list_commands(self, ctx):
        """Dynamically get the list of commands."""
        rv = [] 
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        """Dynamically get the command."""
        ns = {} 
        fn = os.path.join(plugin_folder, name + '.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']

@click.command(cls=CbCLI)
def cli():
    """Simple CLI Interface to interact with the combahton API"""
    pass

if __name__ == '__main__':
    cli()