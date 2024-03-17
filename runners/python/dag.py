import ast
from collections import defaultdict

from pydantic import BaseModel


class Node(BaseModel):
    name: str
    children: list["Node"]
    source_code: str


class DAGs(BaseModel):
    dags: list[Node]


def parse_python_code(source_code: str) -> dict[str, ast.AST]:
    """
    Parses Python source code and returns a dictionary mapping element names to their AST nodes.
    """
    tree = ast.parse(source_code)
    elements = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            elements[node.name] = node
    return elements


def extract_references(elements: dict[str, ast.AST]) -> dict[str, set[str]]:
    """
    Extracts and returns references (as a mapping from element names to sets of names they reference)
    from the AST nodes of the elements.
    """
    references = defaultdict(set)
    for name, node in elements.items():
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and child.id in elements and child.id != name:
                references[name].add(child.id)
    return references


def build_dags(elements: dict[str, ast.AST], references: dict[str, set[str]]) -> list[Node]:
    """
    Builds and returns a list of DAGs from the elements and their references.
    """
    # Create nodes for all elements
    nodes = {name: Node(name=name, children=[], source_code=ast.unparse(node)) for name, node in elements.items()}

    # Populate children based on references
    for name, refs in references.items():
        nodes[name].children = [nodes[ref] for ref in refs]

    # Find roots (nodes without incoming edges)
    all_refs = set(ref for refs in references.values() for ref in refs)
    roots = [node for name, node in nodes.items() if name not in all_refs]

    return roots


def get_dags(source_code: str):
    elements = parse_python_code(source_code)
    refs = extract_references(elements)
    return build_dags(elements, refs)


if __name__ == "__main__":
    with open("output.py", "r") as f:
        dags = DAGs(dags=get_dags(f.read()))
    print(dags.model_dump_json())
