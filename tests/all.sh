#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"

./t_codingstandard.sh
[[ $? -ne 0 ]] && exit 1
