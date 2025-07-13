"""Orquestador principal de Engine-Turbo."""

import aiohttp
import asyncio
from pathlib import Path
from typing import Dict, Any

class EngineTurbo:
    """Clase principal para generar proyectos."""

    def __init__(self, config_path: str = "engine-turbo.json"):
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.session: aiohttp.ClientSession | None = None

    async def init_project(self, name: str, template: str = "saas-basic") -> str:
        """Flujo principal de generación de proyecto."""
        architecture = await self._call_claude(
            f"Design {template} architecture for {name}. Respond in JSON format with entities, api_endpoints, database_schema, features, tech_stack."
        )
        backend_code = await self._call_openai(
            f"Generate complete FastAPI backend code for: {architecture}. Include models, routes, auth, database setup."
        )
        frontend_code = await self._call_deepseek(
            f"Generate complete Next.js frontend with TypeScript for: {architecture}. Include components, pages, API client."
        )
        from .templates import TemplateEngine
        engine = TemplateEngine()
        project_files = engine.render_project(template, {
            "app_name": name,
            "architecture": architecture,
            "generated_backend": backend_code,
            "generated_frontend": frontend_code,
        })
        self._write_project(name, project_files)
        return f"✅ Proyecto {name} creado exitosamente"

    async def _call_claude(self, prompt: str) -> Dict[str, Any]:
        return await self._api_call("claude", prompt)

    async def _call_openai(self, prompt: str) -> str:
        return await self._api_call("openai", prompt)

    async def _call_deepseek(self, prompt: str) -> str:
        return await self._api_call("deepseek", prompt)

    async def _api_call(self, provider: str, prompt: str):
        if not self.session:
            self.session = aiohttp.ClientSession()
        for _ in range(3):
            try:
                # Placeholder simple HTTP POST
                async with self.session.post(f"https://api.{provider}.com/generate", json={"prompt": prompt}) as r:
                    if r.status == 200:
                        data = await r.json()
                        return data.get("content")
            except aiohttp.ClientError:
                await asyncio.sleep(1)
        raise RuntimeError(f"{provider} API request failed")

    def _write_project(self, name: str, files: Dict[str, str]):
        base = Path(name)
        for path, content in files.items():
            file_path = base / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)

    def _load_config(self, path: str) -> Dict[str, Any]:
        cfg_path = Path(path)
        if cfg_path.exists():
            import json
            return json.loads(cfg_path.read_text())
        return {}
