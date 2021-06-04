#!/bin/sh

export PIPENV_PIPFILE=../mockdown/Pipfile
LOGLEVEL=INFO
timeout 180 pipenv run -- mockdown run -pb 1400 2520 1480 2600 -pm hierarchical --learning-method noisetolerant ../mockdown-inferui-eval/tmp/2298_input.json ../mockdown-inferui-eval/tmp/2298_output.json
