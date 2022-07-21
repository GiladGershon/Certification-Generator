# -------------------------------------------------------------------------
# Made with LOVE By Gilad Gershon
# Licensed under the MIT License.
# --------------------------------------------------------------------------
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('-a', '--address', type=str, default='0.0.0.0')
@click.option('-p', '--port', type=int, default=80)
@click.option('-d', '--debug', type=bool, default=False)
def webapp(address, port, debug):
    """web app"""
    from webapp import app
    app.run(address, port, debug)


if __name__ == '__main__':
    cli()
