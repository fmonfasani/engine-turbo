from engine_turbo.core import EngineTurbo
import asyncio

engine = EngineTurbo()
print(asyncio.run(engine.init_project("my-saas")))
