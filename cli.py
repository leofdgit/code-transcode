import json
import os
import subprocess

import click

from src.cli import AsyncClickCommand, file_to_str
from src.config import load_config
from src.eval import CompareResult, Result, compare_results
from src.openai_client import OpenAIClient
from src.transcoder import ProgrammingLanguage, Transcoder


def get_builder(lang: ProgrammingLanguage) -> str:
    match lang.value:
        case "python":
            return "runners/python/py.Dockerfile"
        case "javascript":
            return "runners/nodejs/js.Dockerfile"
        case _:
            raise ValueError(f"Cannot find builder for language {lang}")


@click.command(cls=AsyncClickCommand)
@click.argument("input_file", type=click.STRING)
@click.argument("input_language", type=click.Choice(ProgrammingLanguage))
@click.argument("output_file", type=click.STRING)
@click.argument("output_language", type=click.Choice(ProgrammingLanguage))
@click.option("--num-iterations", "-n", type=click.INT, default=3)
async def transcode(
    input_file: str,
    input_language: ProgrammingLanguage,
    output_file: str,
    output_language: ProgrammingLanguage,
    num_iterations: int = 3,
):
    """
    Transcode code from one language to another.
    """
    # Generate code
    input_code = file_to_str(input_file)
    # TODO: support other AI providers?
    ai_client = OpenAIClient(load_config())
    transcoder = Transcoder(ai_client)
    output_code = await transcoder(input_code, input_language, output_language)
    with open(output_file, "w") as f:
        f.write(output_code)
    # Run input and output code
    input_results_path = "input_results.dat"
    output_results_path = "output_results.dat"
    for _ in range(num_iterations):
        subprocess.run(
            [f"./run.sh {get_builder(input_language)} {input_results_path}"],
            shell=True,
            check=True,
        )
        subprocess.run(
            [f"./run.sh {get_builder(output_language)} {output_results_path}"],
            shell=True,
            check=True,
        )
        # Compare results
        with open(input_results_path, "r") as f:
            base_results = f.readlines()
            base_results = [Result(result=json.loads(r)) for r in base_results]
        with open(output_results_path, "r") as f:
            new_results = f.readlines()
            new_results = [Result(result=json.loads(r)) for r in new_results]
        results_file = "compare_results.dat"
        with open("test_cases.dat", "r") as f:
            test_cases = [json.loads(line) for line in f.readlines()]
        with open(results_file, "w") as f:
            for r in compare_results(
                base_results,
                new_results,
                test_cases,
            ):
                f.write(f"{r.model_dump_json()}\n")
        # If there are no errors then return, else repeat
        if os.path.exists(results_file) and os.path.getsize(results_file) > 0:
            with open(results_file, "r") as f:
                discrepencies = [CompareResult(**json.loads(line)) for line in f.readlines()]
            output_code = await transcoder.iterate(
                input_language, input_code, output_language, output_code, discrepencies
            )
            with open(output_file, "w") as f:
                f.write(output_code)
        else:
            return


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
    with open("compare_results.dat", "w") as f:
        for r in compare_results(base_results, new_results):
            f.write(r.model_dump_json())


@click.group()
def cli():
    pass


cli.add_command(transcode)
cli.add_command(eval)

if __name__ == "__main__":
    cli()
