@echo off
chcp 65001 > nul
git add .
git diff --staged > .diff