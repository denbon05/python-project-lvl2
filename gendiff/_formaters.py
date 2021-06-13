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
        return get_json_diff(nodes, deep + 1)
    return value


def handle_ast(ast, format):
    foramters = {
        "stylish": get_json_diff(ast),
    }
    return foramters[format]


def get_json_diff(ast, deep=0, separater="  "):
    if isinstance(ast, list):
        return "{{{tree}\n{separ}}}".format(
            tree=''.join(map(lambda n: get_json_diff(n, deep + 1), ast)),
            separ=deep * separater,
        )
    tokens = {
        "equal": "  ",
        "added": "+ ",
        "deleted": "- ",
    }

    full_separater = deep * separater
    status = ast.get("status", "equal")
    children = ast.get("children", [])
    value = (
        get_json_diff(children, deep + 1) if children
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
