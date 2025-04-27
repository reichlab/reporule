# reporule

A utility for standardizing repository settings within a GitHub organization.

## Using reporule: GitHub workflows

The easiest way to use reporule is to run one of the GitHub workflows included
in the project's repository:

- no need to clone the repository
- no need to generate a GitHub personal access token

## Using reporule: command line interface (CLI)

You can also use reporule as a CLI.

```bash
➜ uv run reporule --help

 Usage: reporule [OPTIONS] COMMAND [ARGS]...

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────╮
│ list                                                                                               │
│ ruleset                                                                                            │
│ security                                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Setup

These instructions assume that you have
[uv](https://docs.astral.sh/uv/getting-started/installation/) installed
(uv will handle any required Python installs and virtual environments).

reporule is not released on PyPI, so you will need to install it from GitHub

```bash
uv venv
uv pip install git+https://github.com/reichlab/reporule
```

To use the CLI, you will you need a GitHub personal access token with the following
permissions:

1. Follow these
   [GitHub directions for creating a fine-grained personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)
2. In the _Repository access_ section, choose _All repositories_ (this will
   give the token access to the same repository permissions that your
   personal GitHub account has)
3. In the _Permissions_ section, expand the _Repository permissions_ section
4. Find _Administration_ on list set its _Access_ to _Read and write_
5. Click _Generate token_ at bottom of the page
6. Click _Generate token_ again when prompted
7. You should now see your new access token. Copy the value and save it
   somewhere safe.
8. In your local machine's terminal, save the token in an environment variable called `GITHUB_TOKEN`:

    ```bash
    export GITHUB_TOKEN=your_new_github_token
    ```
