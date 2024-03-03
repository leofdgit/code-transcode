from typing import Union, Literal

from pydantic import BaseModel, Field

type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


class ValueResult(BaseModel):
    result: Literal["success"]
    output: JSON


class ErrorResult(BaseModel):
    result: Literal["failure"]
    output: JSON


class Result(BaseModel):
    result: Union[ValueResult, ErrorResult] = Field(discriminator="result")


class CompareResult(BaseModel):
    idx: int
    diff_type: Union[Literal["result"], Literal["output"]]


def compare_results(
    base_results: list[Result], new_results: list[Result]
) -> list[CompareResult]:
    if (num_base_results := len(base_results)) != (num_new_results := len(new_results)):
        raise ValueError(
            f"Got {num_base_results} base test results and {num_new_results} new test results."
        )

    output: list[CompareResult] = []
    for i, (br, nr) in enumerate(zip(base_results, new_results)):
        if br.result.result != nr.result.result:
            output.append(CompareResult(idx=i, diff_type="result"))
        elif br.result.result == "success" and br.result.output != nr.result.output:
            output.append(CompareResult(idx=i, diff_type="output"))
    return output
