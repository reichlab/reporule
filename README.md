# reporule

A utility for standardizing repository settings within a GitHub organization.

## Overview

reporule is a command line interface (CLI) with two commands:

- `list`: display a list of repos associated with a given GitHub org or user
- `ruleset`: apply a pre-defined GitHub branch ruleset:

    - to all repos for a GitHub org or user
    - a single GitHub repo

### Setup (one time)

- Install `[uv](https://docs.astral.sh/uv/getting-started/installation/)` to manage the Python installs and environment
- Create a fine-grained personal GitHub token

   1. Follow these
      [GitHub directions for creating a fine-grained personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)
   2. In the _Repository access_ section, choose _All repositories_ (this will
      give the token access to the same repository permissions that your
      personal GitHub account has)
   3. In the _Permissions_ section, expand the _Repository permissions_ section
   4. Find _Administration_ on list set its _Access_ to _Read and write_
   5. Click _Generate token_ at bottom of the page
   6. Click _Generate token_ again when prompted

- Save the GitHub token as an environment variable called `GITHUB_TOKEN`

## Using reporule

To use the reporule CLI, you can either install the Python package locally, or
use [uv's tool feature](https://docs.astral.sh/uv/guides/tools/) to run the CLI
without an explicit install.

For brevity, the examples in this readme work for a locally-installed package.

### Install locally

If you're comfortable installing Python packages, you can install `reporule` from GitHub. The most
straightforward way to do this is via `uv`, which will handle setting up a virtual environment,
installing Python (if required), and installing the package and its dependencies.

```bash
uv venv
uv pip install git+https://github.com/reichlab/reporule
```

In this case, CLI commands are prefixed by `uv run`. For example, to access the main CLI help:

```bash
uv run reporule --help
```

### Run CLI without installing the package

If you'd prefer not to install YAPP (Yet Another Python Package), you can use
[uv's tool feature](https://docs.astral.sh/uv/guides/tools/) to run the reporule CLI
transiently ("in the background") without an explicit install.

In this case, CLI commands are prefixed by `uvx git+https://github.com/reichlab/reporule`.
For example, to access the main CLI help:

```bash
uvx git+https://github.com/reichlab/reporule --help
```

The incantation is a bit unwieldy, but using `uvx` will run the latest version of the code from
GitHub, without you needed to worrying about installs of upgrade.

## List repos command

## Ruleset command
