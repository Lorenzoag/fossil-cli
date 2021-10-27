from pathlib import Path

from click import command, option

from .utils import checkbox, echo, error, fossil, prompt, run


@command()
@option("-n", "--name", type=str, help="Nombre del repositorio")
@option("-f", "--filename", type=Path, help="Archivo del repositorio")
@option("-r", "--readme", type=Path, help="Nombre del archivo readme")
@option("-v", "--version", type=Path, help="Version Inicial", default="0.0.0")
def new(name, filename, readme, version):
    """
    Crea un nuevo repositorio.
    """
    print(version)

    repo = filename or Path(prompt("Archivo del repositorio", default=".fossil"))
    if repo.is_absolute():
        error(f"{repo} no es relativo")
    if repo.exists():
        error(f"Ya existe el repositorio {repo}")

    name = name or prompt("Nombre del repositorio", default=Path().absolute().name)
    readme = readme or prompt("Nombre del archivo readme", default="README.md")

    # Create the repo
    run(f"{fossil} init {repo}")

    # Updating parameters
    run(
        f'''{fossil} sqlite "insert or replace into config values ('project-name', '{name}', now());" -R "{repo}"'''
    )
    run(
        f'''{fossil} sqlite "insert or replace into config values ('index-page', '/doc/tip/{readme}', now());" -R "{repo}"'''
    )

    # Opening the repo
    run(f"{fossil} open --force {repo}")

    # Append initial files
    choices = run(f"{fossil} extras --ignore *.pyc").splitlines()
    files = checkbox("Escoja los archivos iniciales", choices=choices)
    run(f"{fossil} add {' '.join(files)}")
    run(f'{fossil} commit -m "Initial Commit" --no-warnings')
    run(f"{fossil} tag add v{version} trunk")

    # Create developer branch
    run(f"{fossil} branch new develop trunk")
    run(f"{fossil} tag add v{version} develop")
    run(f"{fossil} update develop")
