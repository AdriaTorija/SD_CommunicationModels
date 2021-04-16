import xmlrpc.client
import click
@click.group()
def main():
    pass

@main.command()
@click.argument('x', type=click.INT)
def create(x):
    click.echo(proxy.create_worker(x))

@main.command()
@click.argument('x',type=click.INT)
def delete(x):
    click.echo(proxy.delete_worker(x))

def list():
    click.echo(proxy.list())


if __name__ == '__main__':
    proxy=xmlrpc.client.ServerProxy('http://localhost:8000')
    main()