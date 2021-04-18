import xmlrpc.client
import click

@click.group()
def worker():
    pass

@click.group()
def job():
    pass

@worker.command()
def create():
    click.echo(proxy.create_worker())

@worker.command()
@click.argument('x', type=click.INT)
def delete(x):
    click.echo(proxy.delete_worker(x))

@worker.command()
def list():
    click.echo(proxy.list_workers())

@job.command()
@click.argument('func', nargs=-1)
@click.argument('arguments', nargs=1)
def work():
    click.echo(proxy.work)

if __name__ == '__main__':
    proxy=xmlrpc.client.ServerProxy('http://localhost:8000')
    worker()