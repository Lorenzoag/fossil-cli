from pathlib import Path

from click import command, option

from .utils import checkbox, confirm, echo, error, fossil, prompt, run, select
from .Version import get_version


@command()
def branch():
    """
    Manipula los ramas convenientemente
    """

    current_branch = run(f"{fossil} branch current")
    version = get_version(current_branch)

    echo(f"Rama actual     {current_branch}")
    echo(f"Version actual  {version}")

    if run(f"{fossil} changes"):
        error("Existen cambios realice un commit primero")

    if current_branch == "trunk":
        version = version.next_version("patch")
        br_name = "hotfix-" + prompt("Escriba nombre de la rama")

        if confirm(f"Estas seguro de crear la rama {br_name}?"):
            run(f"{fossil} branch new {br_name} {current_branch}")
            run(f"{fossil} tag add v{str(version)} {br_name}")
            run(f"{fossil} update {br_name}")

    elif current_branch == "develop":
        branchs = [
            "feature: Una rama para agregar una caracteristica",
            "release: Una rama para arregrar el codigo antes de publicarlo",
            "cancelar: Cancelando la operacion",
        ]

        branch = select("Selecciona el tipo de rama a crear:", choices=branchs)

        if branch.startswith("cancelar"):
            error("Cancelando")

        if branch.startswith("feature"):
            br_name = "feature-" + prompt("Escriba nombre de la rama")
            version = version.next_version("minor").next_version("prerelease", "dev")
        else:
            br_name = f"release-{str(version)}"
            version = version.next_version("prerelease")

        if confirm(f"Estas seguro de crear la rama {br_name}?"):
            run(f"{fossil} branch new {br_name} {current_branch}")
            run(f"{fossil} tag add v{str(version)} {br_name}")
            run(f"{fossil} update {br_name}")

    elif current_branch.startswith("feature"):
        version = version.finalize_version()
        if confirm(f"Estas seguro de unificar la rama {current_branch} en develop?"):
            run(f"{fossil} update develop")
            run(f"{fossil} merge --integrate {current_branch}")
            run(
                f'{fossil} commit -m "Unificando la rama {current_branch}" --no-warnings'
            )
            run(f"{fossil} tag add v{str(version)} develop")

            if confirm(f"Deseas unificar la rama develop en trunk?"):
                run(f"{fossil} update trunk")
                run(f"{fossil} merge develop")
                run(f'{fossil} commit -m "Unificando la rama develop" --no-warnings')
                run(f"{fossil} tag add v{str(version)} trunk")

                if confirm(f"Deseas regresar a la rama develop?"):
                    run(f"{fossil} update develop")

    elif current_branch.startswith("release"):
        version = version.finalize_version()
        if confirm(f"Estas seguro de cerrar la version {version}?"):
            run(f"{fossil} update develop")
            run(f"{fossil} merge --integrate {current_branch}")
            run(
                f'{fossil} commit -m "Unificando la rama {current_branch}" --no-warnings'
            )
            run(f"{fossil} tag add v{str(version)} develop")

            run(f"{fossil} update trunk")
            run(f"{fossil} merge develop")
            run(f'{fossil} commit -m "Unificando la rama develop" --no-warnings')
            run(f"{fossil} tag add v{str(version)} trunk")

            if confirm(f"Deseas regresar a la rama develop?"):
                run(f"{fossil} update develop")

    elif current_branch.startswith("hotfix"):
        version = version.finalize_version()

        if confirm(f"Estas seguro de unificar la rama {current_branch} en develop?"):
            run(f"{fossil} update develop")
            run(f"{fossil} merge --integrate {current_branch}")
            run(
                f'{fossil} commit -m "Unificando la rama {current_branch}" --no-warnings'
            )
            run(f"{fossil} tag add v{str(version)} develop")

            if confirm(f"Deseas unificar la rama develop en trunk?"):
                run(f"{fossil} update trunk")
                run(f"{fossil} merge develop")
                run(f'{fossil} commit -m "Unificando la rama develop" --no-warnings')
                run(f"{fossil} tag add v{str(version)} trunk")

                if confirm(f"Deseas regresar a la rama develop?"):
                    run(f"{fossil} update develop")
