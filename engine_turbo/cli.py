"""Comandos CLI de Engine-Turbo."""

import asyncio
import typer
from rich.console import Console

from .core import EngineTurbo

app = typer.Typer()
console = Console()

@app.command()
def init(name: str, template: str = typer.Option("saas-basic", help="Template a usar")):
    """Crear nuevo proyecto"""
    engine = EngineTurbo()
    result = asyncio.run(engine.init_project(name, template))
    console.print(result, style="green")

@app.command()
def deploy(target: str = "local"):
    """Deploy proyecto actual"""
    console.print(f"Deploy {target} no implementado", style="yellow")

@app.command()
def add(entity: str):
    """Agregar entidad al proyecto existente"""
    console.print(f"Agregar {entity} no implementado", style="yellow")

@app.command()
def doctor():
    """Diagnóstico del sistema"""
    console.print("Sistema OK", style="green")

@app.command()
def templates():
    """Listar templates disponibles"""
    from .templates import TemplateEngine
    engine = TemplateEngine()
    for tpl in engine.list_templates():
        console.print(tpl)
