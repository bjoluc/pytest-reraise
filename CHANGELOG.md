# Changelog

All notable changes to this project will be documented in this file. See
[Conventional Commits](https://conventionalcommits.org) for commit guidelines.

### [2.1.1](https://github.com/bjoluc/pytest-reraise/compare/v2.1.0...v2.1.1) (2021-06-17)


### Bug Fixes

* **Plugin:** Prevent an `AttributeError` when pytest-reraise is used alongside non-test plugins like pytest-black or pytest-flake8. Thanks [@jcpunk](https://github.com/jcpunk)! ([adadd8a](https://github.com/bjoluc/pytest-reraise/commit/adadd8aee2e159cb052c00ccd82802f0ab9a2e27))

## [2.1.0](https://github.com/bjoluc/pytest-reraise/compare/v2.0.0...v2.1.0) (2021-06-09)


### Features

* Introduce `reraise.wrap()` method to simplify function wrapping ([f245ffd](https://github.com/bjoluc/pytest-reraise/commit/f245ffdcaf667936c3a9265b1469690fc87bf4eb))

## [2.0.0](https://github.com/bjoluc/pytest-reraise/compare/v1.0.3...v2.0.0) (2021-06-03)


### ⚠ BREAKING CHANGES

* Python 3.5 is no longer officially supported.

### Bug Fixes

* Do not rewrite assertions in `pytest_reraise.reraise` ([620f1a0](https://github.com/bjoluc/pytest-reraise/commit/620f1a0232e5a855908755948106526a6b4694a7))


### Continuous Integration

* Run tests against a set of pytest versions ([913f22b](https://github.com/bjoluc/pytest-reraise/commit/913f22b8c69d259b5c5d16a9d9625be927ebbc35))

## 1.0.3 (2020-06-03)

### Fix

- **Packaging**: Add missing classifiers

## 1.0.2 (2020-06-03)

### Refactor

- **Core**: Sort imports

## 1.0.1 (2020-05-17)

### Fix

- **Core**: Don't re-raise if the test case itself has already re-raised
- **Concurrency**: Make exception access thread-safe

## 1.0.0 (2020-05-17)

### Fix

- **Typing**: Remove member type annotations (not supported by Python 3.5)
