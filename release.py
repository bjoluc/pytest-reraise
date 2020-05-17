"""
Script to optionally do an automated release using commitizen and poetry. 

Environment variables:
* POETRY_PYPI_TOKEN_PYPI
* GH_TOKEN
"""

import argparse
import os
import subprocess
from typing import List

parser = argparse.ArgumentParser()
parser.add_argument("--publish", action="store_true")
options = parser.parse_args()

IS_DRY_RUN = not options.publish


def call(args: List[str]) -> str:
    output = subprocess.check_output(args, universal_newlines=True)
    return output.rstrip("\n")


def get_current_version():
    return call(["cz", "version", "--project"])


print("Getting current version...")
initial_version = get_current_version()
print("Current version: " + initial_version)


bump_args = [
    "--yes",
    "--check-consistency",
    "--changelog",
]

if IS_DRY_RUN:
    bump_args += ["--dry-run"]

if initial_version.startswith("0."):
    print("Current major version is 0. Bumping to 1 and creating initial release.")
    bump_args += ["--increment", "MAJOR"]

    if not IS_DRY_RUN:
        print("Creating CHANGELOG.md...")
        subprocess.run(["touch", "CHANGELOG.md"])
        subprocess.run(["git", "add", "CHANGELOG.md"])

print("\nRunning cz bump...")
subprocess.run(["cz", "bump"] + bump_args)

new_version = get_current_version()

if new_version == initial_version:
    print("Version not changed.")
    exit(0)

print("\nVersion changed to " + new_version)

if IS_DRY_RUN:
    exit(0)

print("\nPushing to git repository...")

origin = "origin"
if "TRAVIS" in os.environ:
    if "GH_TOKEN" not in os.environ:
        print("GH_TOKEN environment variable not set.")
        exit(1)

    origin = "https://{}@github.com/{}.git".format(
        os.environ["GH_TOKEN"], os.environ["TRAVIS_REPO_SLUG"]
    )

subprocess.run(["git", "push", origin, "HEAD:master", "--follow-tags", "--tags"])

print("\nPublishing to pypi...")
subprocess.run(["poetry", "publish", "--build"])
