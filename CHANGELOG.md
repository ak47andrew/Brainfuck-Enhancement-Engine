# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `put` function that works just like `print`, but without newline
- Support for chars (strings with one character in it)

## [0.1.1]

### Fixed
- Fixed an issue where you could set value out of 0-255 range and loaded value would overflow

## [0.1.0] - 2025-09-30

### Added
- **First Alpha Release**: Basic compiler pipeline is now functional!
- Complete compilation flow: BEE → Intermediate Language → NJ → Brainfuck
- Tokenizer and parser for BEE syntax
- Intermediate Language (IL) representation
- Custom Brainfuck interpreter/runner
- IL to NJ language translation
- `print` function with automatic newline
- Support for integers (0-255 range)
- CLI with `--debug` flag for development
- Initial project structure and documentation

## [0.0.1] - 2025-09-20

### Added
- Initial commit for the new implementation of BEE compiler. For more info check corresponding 
[devlog](docs/devlog/DEVLOG-0001-rewrite.md)