import asyncio

import click


def file_to_str(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()


class AsyncClickCommand(click.Command):
    def invoke(self, ctx):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.callback(**ctx.params))
