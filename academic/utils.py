from pathlib import Path


def hugo_in_docker_or_local():
    """Checks if there's a `docker-compose.yml` in local directory. If so, prefer that
    to a local hugo installation.
    """
    if Path().glob("docker-compose.yml"):
        hugo = "docker-compose run hugo"
    else:
        hugo = ""

    return " ".join([hugo, "hugo"])
