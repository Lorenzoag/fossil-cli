from click import command

from .utils import confirm, echo, error, fossil, prompt, run, run_pre_pos, select
from .Version import get_version


@command()
def commit():
    """
    Corre un commit al repositorio.
    """
    current_branch = run(f"{fossil} branch current")

    if current_branch in ("trunk", "develop"):
        error("Los cambios se deben realizar en una rama dedicada")

    if not run(f"{fossil} changes"):
        error("No existen cambios")

    version = get_version(current_branch)

    echo(f"Rama actual     {current_branch}")
    echo(f"Version actual  {version}")

    if current_branch.startswith("feature-") or current_branch.startswith("hotfix-"):
        version = version.next_version("prerelease", "dev")
    elif current_branch.startswith("release-"):
        version = version.next_version("prerelease")

    changes = {
        "new: Una nueva caracteristica": [
            "feat: Adicionando una caracteristica",
            "docs: Adicionando la documentacion",
            "test: Adicionando pruebas",
        ],
        "changes: Cambio que mejora el codigo en general": [
            "docs: Cambio solo en la documentacion",
            "style: Cambio que afectan el estilo del codigo",
            "refactor: El codigo cambia pero no corrige un bug o es una nueva caracteristica",
            "perf: Cambio que mejora el codigo en general",
            "build: Cambios que afecta el sistema de build o las librerias externas",
            "ci: Cambios sobre los script CI o sobre el sistema",
        ],
        "fixes: Arreglo de bugs": [
            "fix: Arreglo de bugs",
            "build: Arreglo de bugs que afecta el sistema de build o las librerias externas",
            "ci: Arreglo de bugs sobre los script CI o sobre el sistema",
        ],
        "breaks: Eliminando codigo no usado": [
            "feat: Eliminando una caracteristica",
            "docs: Eliminando la documentacion",
            "test: Eliminando pruebas",
        ],
        "cancelar: Cancelando la operacion": [],
    }

    change_type = select(
        "Selecciona el tipo de cambio del commit:", choices=changes.keys()
    )
    if change_type.startswith("cancelar"):
        error("Cancelando")
    change_concept = select(
        "Selecciona el concepto de cambio del commit:",
        choices=changes[change_type],
    ).split(":")[0]
    change_type = change_type.split(":")[0]
    change_body = prompt("Escriba el cuerpo del commit")

    commit = f"{change_type}({change_concept}): {change_body}"

    if confirm("Estas seguro de aplicar el commit?"):
        run_pre_pos("pre_commit", **locals())

        run(f'{fossil} commit -m "{commit}" --no-warnings')
        run(f"{fossil} tag add v{str(version)} {current_branch}")

        run_pre_pos("pos_commit", **locals())
