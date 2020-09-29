import os
import ast
import glob
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


SPACE  = '    '
BRANCH = '│   '
TEE    = '├── '
LAST   = '└── '

def print_tree(exports):
    print(f'./{LIB}/')
    ptrs = [TEE] * (len(exports) - 1) + [LAST]
    for ptr, module in zip(ptrs, exports.keys()):
        print(f'{ptr}{module}')
        p = BRANCH if ptr == TEE else SPACE
        xs = [f'{p}{TEE}{o}' for o in exports[module][:-1]] + [f'{p}{LAST}{exports[module][-1]}']
        print('\n'.join(xs))

print_tree(exports)