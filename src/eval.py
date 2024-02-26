from typing import Union, Literal

from pydantic import BaseModel, Field

type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


class ValueResult(BaseModel):
    type: Literal["Value"]
    value: JSON


class ErrorResult(BaseModel):
    type: Literal["Error"]


class Result(BaseModel):
    result: Union[ValueResult, ErrorResult] = Field(discriminator="type")


class CompareResult(BaseModel):
    idx: int
    diff_type: Union[Literal["type"], Literal["value"]]


def compare_results(
    base_results: list[Result], new_results: list[Result]
) -> list[CompareResult]:
    if (num_base_results := len(base_results)) != (num_new_results := len(new_results)):
        raise ValueError(
            f"Got {num_base_results} base test results and {num_new_results} new test results."
        )

    output: list[CompareResult] = []
    for i, (br, nr) in enumerate(zip(base_results, new_results)):
        if br.result.type != nr.result.type:
            output.append(CompareResult(idx=i, diff_type="type"))
        elif br.result.type == "Value" and br.result.value != nr.result.value:
            output.append(CompareResult(idx=i, diff_type="value"))
    return output
