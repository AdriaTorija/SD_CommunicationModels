import xmlrpc.client
import click

@click.group()
def main():
    pass

@main.command()
def create():
    click.echo(proxy.create_worker())

@main.command()
@click.argument('x', type=click.INT)
def delete(x):
    click.echo(proxy.delete_worker(x))

@main.command()
def list():
    click.echo(proxy.list_workers())

@main.command()
@click.argument('func', type=click.STRING, nargs=1)
@click.argument('arguments', nargs=-1)
def job(func, arguments):
    click.echo(proxy.create_task(func, arguments))

@main.command()
def result():
    click.echo(proxy.get_result())

if __name__ == '__main__':
    proxy=xmlrpc.client.ServerProxy('http://localhost:8000')
    main()