#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"
source prepare.sh

echo "Checking code style using pep8"
pep8 ../mcwrapper
if [[ $? == 0 ]]; then
	echo "Ok"
else
	exit 1
fi

echo "Checking for common errors"
pyflakes ../mcwrapper
if [[ $? == 0 ]]; then
	echo "Ok"
else
	exit 1
fi

# This test is not part of standard check because of errors caused by dynamic variable
# loading to configuration. But it should be run from time to time to found other mistakes
#echo "Checking bugs and poor quality"
#pylint --reports=n ../mcwrapper
