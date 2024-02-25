import click
from src.cli import file_to_str, AsyncClickCommand
from src.config import load_config
from src.transcoder import InputLanguage, OutputLanguage, Transcoder
from src.openai_client import OpenAIClient


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
    input_code = file_to_str(input_file)
    # TODO: support other AI providers?
    ai_client = OpenAIClient(load_config())
    transcoder = Transcoder(ai_client)
    output_code = await transcoder(input_code, input_language, output_language)
    with open(output_file, "w") as f:
        f.write(output_code)


@click.group()
def cli():
    pass


cli.add_command(transcode)

if __name__ == "__main__":
    cli()
