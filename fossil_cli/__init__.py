from click import group

from .Branch import branch
from .Commit import commit
from .Info import info
from .New import new
from .Version import version


@group()
def cli():
    pass


cli.add_command(new)
cli.add_command(new, "init")

cli.add_command(version)
cli.add_command(version, "v")

cli.add_command(info)

cli.add_command(commit)
cli.add_command(commit, "c")

cli.add_command(branch)
cli.add_command(branch, "br")
