import io
from json import loads
from os.path import splitext

import yaml


def get_diff_ast(node1: dict, node2: dict):  # noqa: C901
    def build_ast(n1, n2):
        entries = {**n1, **n2}
        ast = []
        for key, value in entries.items():
            node = {}
            ast.append(node)
            n1_value = n1.get(key, {})
            n2_value = n2.get(key, {})
            node["key"] = key
            node["value"] = value
            if key in n1 and key not in n2:
                node["status"] = "deleted"
            elif key in n2 and key not in n1:
                node["status"] = "added"
            elif n1_value != n2_value:
                if is_complex(n1_value) and is_complex(n2_value):
                    node["children"] = build_ast(n1_value, n2_value)
                    node["status"] = "equal"
                else:
                    node["status"] = "changed"
                    node["old_value"] = n1_value
            else:
                node["status"] = "equal"
        return sorted(ast, key=lambda n: n["key"])

    return build_ast(node1, node2)


def get_parsed_data(filepath):
    ext = splitext(filepath)[1]
    handlers = {
        ".json": lambda fpath: loads(io.open(fpath).read()),
        ".yml": lambda fpath: yaml.load(
            io.open(fpath).read(), Loader=yaml.FullLoader
        ),
        ".yaml": lambda fpath: yaml.load(
            io.open(fpath).read(), Loader=yaml.FullLoader
        ),
    }
    return handlers[ext](filepath)


def is_complex(value):
    return isinstance(value, dict) and value != {}
