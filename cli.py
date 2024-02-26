import click
from src.cli import file_to_str, AsyncClickCommand
from src.config import load_config
from src.eval import compare_results, Result
from src.transcoder import InputLanguage, OutputLanguage, Transcoder
from src.openai_client import OpenAIClient

import json


@click.command(cls=AsyncClickCommand)
@click.argument("input_file", type=click.STRING)
@click.argument("input_language", type=click.Choice(InputLanguage))
@click.argument("output_file", type=click.STRING)
@click.argument("output_language", type=click.Choice(OutputLanguage))
async def transcode(
    input_file: str,
    input_language: InputLanguage,
    output_file: str,
    output_language: OutputLanguage,
):
    """
    Transcode code from one language to another.
    """
    input_code = file_to_str(input_file)
    # TODO: support other AI providers?
    ai_client = OpenAIClient(load_config())
    transcoder = Transcoder(ai_client)
    output_code = await transcoder(input_code, input_language, output_language)
    with open(output_file, "w") as f:
        f.write(output_code)


@click.command(cls=AsyncClickCommand)
@click.argument("base_results_path", type=click.STRING)
@click.argument("new_results_path", type=click.STRING)
async def eval(base_results_path: str, new_results_path: str):
    """
    Compare the results of two implementations of a function.
    """
    with open(base_results_path, "r") as f:
        base_results = f.readlines()
        base_results = [Result(result=json.loads(r)) for r in base_results]
    with open(new_results_path, "r") as f:
        new_results = f.readlines()
        new_results = [Result(result=json.loads(r)) for r in new_results]
    return compare_results(base_results, new_results)


@click.group()
def cli():
    pass


cli.add_command(transcode)
cli.add_command(eval)

if __name__ == "__main__":
    cli()
