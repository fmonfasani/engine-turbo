"""Herramientas de deploy básicas."""

from pathlib import Path


def deploy_local(path: str):
    """Deploy usando docker-compose."""
    compose = Path(path) / "docker-compose.yml"
    if compose.exists():
        import subprocess
        subprocess.run(["docker", "compose", "-f", str(compose), "up", "-d"]) 
    else:
        raise FileNotFoundError("docker-compose.yml no encontrado")
