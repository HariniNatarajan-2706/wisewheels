import click

@click.command("hello-app")
def help():
    print("Hello from the custom Bench CLI!")

commands = [help]