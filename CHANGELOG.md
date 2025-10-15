# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3] - 2025-10-15

### Added
- Added two python scripts for visualazing translation process and NJ's execution (second one is still quite buggy tho)

### Changed
- Put all the code into `src` function and made it possible to work as with python's modules

## [0.2.1] - 2025-10-05

### Changed
- Made Token model more stable code-wise by removing nested lists and using args

### Fixed
- Now `print` and `put` functions properly hadle several arguments

## [0.2.0] - 2025-09-30

### Added
- `put` function that works just like `print`, but without newline
- Support for string

### Fixed
- Fixed incorrect tokenizing when using commas in strings
- Fixed incorrect interpreting when having space as a value in LOAD_IMMEDIATE (when you had strings with spaces in it)

## [0.1.1] - 2025-09-30

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
