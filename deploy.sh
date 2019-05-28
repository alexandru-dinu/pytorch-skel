#!/bin/bash

root_dir="$1"

mkdir -p ${root_dir}
for d in configs models src; do cp -r ${d} ${root_dir}; done

# git-related
cp .gitignore ${root_dir}
echo "# ..." > ${root_dir}/README.md

echo "Created workspace in [${root_dir}]"
