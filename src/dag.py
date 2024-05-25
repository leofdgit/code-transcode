from pydantic import BaseModel


class Node(BaseModel):
    name: str
    children: list["Node"]
    source_code: str


class DAGs(BaseModel):
    dags: list[Node]


def dfs(dag: Node, queue: list[Node] = []):
    for c in dag.children:
        dfs(c, queue)
    queue.append(dag)
    return queue


def all_deps_dag_and_names(node: Node) -> tuple[Node, list[str]]:
    def dfs(node: Node) -> tuple[str, list[str]]:
        # Initialize an empty list to collect names of visited nodes
        visited_names = [node.name]
        # For each child, recursively append its source code and collect names
        appended_source = node.source_code
        for child in node.children:
            child_source, child_names = dfs(child)
            appended_source += "\n" + child_source
            visited_names.extend(child_names)
        # Update the node's source code only if it has children
        if node.children:
            node.source_code = appended_source
        return appended_source, visited_names

    # Create a deep copy of the node to preserve the original DAG
    new_node = node.model_copy(deep=True)
    _, visited_names = dfs(new_node)
    return new_node, visited_names
