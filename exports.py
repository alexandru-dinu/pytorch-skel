import ast
import glob
import os
from collections import defaultdict

LIB = 'bagoftools'
VALID_INSTANCES = [ast.FunctionDef, ast.ClassDef]


def is_valid(obj):
    if any((isinstance(obj, inst) for inst in VALID_INSTANCES)):
        if not obj.name.startswith('_'):
            return True
    return False


exports = defaultdict(lambda: [])

for module in glob.glob(f'{LIB}/*.py'):
    with open(module, 'rt') as fh:
        code = fh.read()

    tree = ast.parse(code)

    for obj in tree.body:
        if is_valid(obj):
            exports[os.path.basename(module)].append(obj.name)

SPACE = '    '
BRANCH = '│   '
TEE = '├── '
LAST = '└── '


def print_tree(exports):
    print(f'./{LIB}/')
    ptrs = [TEE] * (len(exports) - 1) + [LAST]
    for ptr, module in zip(ptrs, sorted(exports.keys())):
        print(f'{ptr}{module}')
        p = BRANCH if ptr == TEE else SPACE
        xs = sorted(exports[module])
        print('\n'.join([f'{p}{TEE}{o}' for o in xs[:-1]] + [f'{p}{LAST}{xs[-1]}']))


print_tree(exports)
