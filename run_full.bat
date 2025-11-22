@echo off

python -m src.hive code.bee > test.nj
python src/NJInterpreter/nj.py test.nj

del test.nj