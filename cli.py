import json
import subprocess

import click

from src.cli import AsyncClickCommand, file_to_str
from src.config import load_config
from src.dag import DAGs, Node, all_deps_dag_and_names, dfs
from src.eval import JSON, CompareResult, Result
from src.eval import compare_results as compare_results_
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


def get_extension(lang: ProgrammingLanguage) -> str:
    match lang.value:
        case "python":
            return ".py"
        case "javascript":
            return ".js"
        case _:
            raise ValueError(f"Cannot get extension for language {lang}")


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
    input_code = file_to_str(input_file)
    ai_client = OpenAIClient(load_config())
    transcoder = Transcoder(ai_client)
    input_dags = get_dag(input_language)
    output_refs: dict[str, str] = {}
    with open("test_cases.json", "r") as f:
        test_cases = json.loads(f.read())
    for d in input_dags.dags:
        print("Processing dag...")
        for node in dfs(d):
            print(f"node={node.name}")
            output_code = await transcoder(node.source_code, input_language, output_language)
            output_refs[node.name] = output_code
            with open(output_file, "w") as f:
                f.write(output_code)
            # Run input and output code
            input_results_path = "input_results.dat"
            output_results_path = "output_results.dat"
            node, deps = all_deps_dag_and_names(node)
            create_test_file(node.name, test_cases)
            create_input_file(node, input_language)
            create_output_file(deps, output_refs, output_language)
            for _ in range(num_iterations):
                print(f"Iteration {_}...")
                run_code(input_language, input_results_path, node.name)
                run_code(output_language, output_results_path, node.name)
                compared_results = compare_results(input_results_path, output_results_path)
                # If there are no errors then return, else repeat
                if len(compared_results) == 0:
                    break
                # there's a bug here
                else:
                    if _ == num_iterations - 1:
                        raise RuntimeError(f"Failed to transcode node={node.name}")
                    else:
                        output_code = await transcoder.iterate(
                            input_language, input_code, output_language, output_code, compared_results
                        )
                        with open(output_file, "w") as f:
                            f.write(output_code)
    with open(f"final{get_extension(output_language)}", "w") as f:
        for func in output_refs.values():
            f.write(f"{func}\n")


def compare_results(input_results_path: str, output_results_path: str) -> list[CompareResult]:
    with open(input_results_path, "r") as f:
        base_results = [Result(result=json.loads(r)) for r in f.readlines()]
    with open(output_results_path, "r") as f:
        new_results = [Result(result=json.loads(r)) for r in f.readlines()]
    with open("test_cases.dat", "r") as f:
        test_cases = [json.loads(line) for line in f.readlines()]
    return compare_results_(base_results, new_results, test_cases)


def run_code(language: ProgrammingLanguage, results_path: str, func_name: str):
    subprocess.run(
        [f"./run.sh {get_builder(language)} {results_path} {func_name}"],
        shell=True,
        check=True,
    )


def get_dag(language: ProgrammingLanguage):
    output_path = f"dag-{language.name}.json"
    subprocess.run(
        [f"./rundag.sh {get_builder(language)} {output_path}"],
        shell=True,
        check=True,
    )
    with open(output_path, "r") as f:
        return DAGs(**json.loads(f.read()))


def create_input_file(node: Node, language: ProgrammingLanguage):
    with open(f"output{get_extension(language)}", "w") as f:
        f.write(node.source_code)


def create_output_file(deps: list[str], refs: dict[str, str], language: ProgrammingLanguage):
    with open(f"output{get_extension(language)}", "w") as f:
        f.write("\n".join(refs[d] for d in deps))


def create_test_file(func_name: str, test_cases: dict[str, list[JSON]]):
    with open("test_cases.dat", "w") as f:
        if (func_test_cases := test_cases.get(func_name)) is None:
            f.write("")
        else:
            for t in func_test_cases:
                f.write(f"{json.dumps(t)}\n")


@click.group()
def cli():
    pass


cli.add_command(transcode)

if __name__ == "__main__":
    cli()
