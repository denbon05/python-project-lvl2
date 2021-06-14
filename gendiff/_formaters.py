from json import dumps


def noramlized(value, deep):
    py_types = ("bool", "NoneType")
    if type(value).__name__ in py_types:
        return dumps(value)
    if isinstance(value, dict):
        # print('\nvalue =>', value)
        nodes = list(map(
            lambda n: {"key": n[0], "value": n[1]}, value.items()
        ))
        return get_stylish_diff(nodes, deep + 1)
    return value


def _normalized_plain(value):
    return (
        "[complex value]" if isinstance(value, dict)
        else dumps(value).replace('"', "'")
    )


def handle_ast(ast, format):
    foramters = {
        "stylish": get_stylish_diff(ast),
        "plain": get_plain_diff(ast),
    }
    return foramters[format]


def get_plain_diff(ast, parent_keys=[]):
    if isinstance(ast, list):
        return "\n".join(map(
            lambda n: get_plain_diff(n, parent_keys),
            filter(lambda n: n.get("status") != "equal", ast),
        ))
    status = ast.get("status")
    if status == "nested":
        return get_plain_diff(
            ast.get("children"),
            [*parent_keys, ast.get("key")],
        )
    key = ".".join([*parent_keys, ast.get("key")])
    value = _normalized_plain(ast.get("value"))
    old_value = ""
    if status == "changed":
        old_value = _normalized_plain(ast.get("old_value"))
    cases = {
        "added": f"Property '{key}' was added with value: {value}",
        "deleted": f"Property '{key}' was removed",
        "changed": f"Property '{key}' was updated. From {old_value} to {value}",
    }
    return cases[status]


def get_stylish_diff(ast, deep=0, separater="  "):
    if isinstance(ast, list):
        return "{{{tree}\n{separ}}}".format(
            tree=''.join(map(lambda n: get_stylish_diff(n, deep + 1), ast)),
            separ=deep * separater,
        )
    tokens = {
        "equal": "  ",
        "added": "+ ",
        "deleted": "- ",
        "nested": "  ",
    }

    full_separater = deep * separater
    status = ast.get("status", "equal")
    children = ast.get("children", [])
    value = (
        get_stylish_diff(children, deep + 1) if children
        else noramlized(ast.get("value"), deep)
    )

    return "\n{ind}{t1}{k}: {v1}\n{ind}{t2}{k}: {v2}".format(
        ind=full_separater,
        t1=tokens.get("deleted"),
        k=ast.get("key"),
        v1=noramlized(ast.get("old_value"), deep),
        t2=tokens.get("added"),
        v2=value,
    ) if status == "changed" else "\n{ind}{t}{k}: {v}".format(
        ind=full_separater,
        t=tokens.get(status),
        k=ast.get("key"),
        v=value,
    )
