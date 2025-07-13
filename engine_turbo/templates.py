"""Motor de templates simple para Engine-Turbo."""

from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import Dict, Any
import yaml

class TemplateEngine:
    def __init__(self, templates_path: str = "templates"):
        self.templates_path = Path(templates_path)
        self.env = Environment(loader=FileSystemLoader(templates_path))

    def list_templates(self) -> list[str]:
        return [p.name for p in self.templates_path.iterdir() if p.is_dir()]

    def render_project(self, template_name: str, context: Dict[str, Any]) -> Dict[str, str]:
        cfg = self.load_template_config(template_name)
        rendered: Dict[str, str] = {}
        for target, src in cfg["files"].items():
            template = self.env.get_template(f"{template_name}/{src}")
            rendered[target] = template.render(context)
        return rendered

    def load_template_config(self, template_name: str) -> Dict[str, Any]:
        path = self.templates_path / template_name / "template.yml"
        with open(path) as f:
            return yaml.safe_load(f)
