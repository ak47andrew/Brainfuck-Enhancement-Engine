#!/bin/bash

python -m bee code.bee > brainfCustomInterpreter/test.bf
python brainfCustomInterpreter/brainfuck.py brainfCustomInterpreter/test.bf