from typing import Literal, Union

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
    test_case: JSON
    diff_type: Union[Literal["result"], Literal["output"]]
    base_output: JSON
    new_output: JSON


def compare_results(
    base_results: list[Result], new_results: list[Result], test_cases: list[JSON]
) -> list[CompareResult]:
    if (num_base_results := len(base_results)) != (num_new_results := len(new_results)):
        raise ValueError(f"Got {num_base_results} base test results and {num_new_results} new test results.")

    output: list[CompareResult] = []
    for br, nr, test in zip(base_results, new_results, test_cases):
        if br.result.result != nr.result.result:
            output.append(CompareResult(test_case=test, diff_type="result", base_output=br, new_output=nr))
        elif br.result.result == "success" and br.result.output != nr.result.output:
            output.append(CompareResult(test_case=test, diff_type="output", base_output=br, new_output=nr))
    return output
