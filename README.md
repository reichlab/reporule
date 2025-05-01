# reporule

A CLI for standardizing GitHub repository branch rulesets.

## Overview

reporule is a command line interface (CLI) with two commands:

- `list`: display a list of repos associated with a given GitHub org or user
- `ruleset`: apply a pre-defined GitHub branch ruleset:

    - to all repos for a GitHub org or user
    - a single GitHub repo

### Setup (one time)

> [!NOTE]
> To use the reporule [`ruleset` command](#ruleset-command), you need admin
> access to the repos being updated (collaborator status is not
> sufficient). Organization owners can add rulesets, as can members of
> a team assigned to the `all-repository-admin` role. \
> [More information](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).

1. Install `[uv](https://docs.astral.sh/uv/getting-started/installation/)` to manage the Python installs and environment
2. Create a GitHub personal access token
3. Create a fine-grained personal GitHub token (classic)

   1. Follow these
      [GitHub directions for creating a classic personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)
   2. On the _New personal access token (classic)_ page, select the following scopes:
      - `repo` (full control of private repositories)
      - `write:org` (in the `admin:org` section)
   3. Click _Generate token_ at bottom of the page

4. Save the GitHub token as an environment variable called `GITHUB_TOKEN`

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

This command lists all public repositories associated with a specific GitHub user or organization. We used a
version of this in the past when auditing repositories in the `reichlab` GitHub org to review potential project
to archive, for example.

```bash
➜ uv run reporule list --help

 Usage: reporule list [OPTIONS] ORG


 Display a list of public repositories and their
 selected attributes for a specific GitHub
 organization or user.

 EXAMPLE:
 --------
 reporule list hubverse-org

╭─ Arguments ───────────────────────────────────────────────╮
│ *    org      TEXT  [default: None] [required]            │
╰───────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────╮
│ --help          Show this message and exit.               │
╰───────────────────────────────────────────────────────────╯
```

For example, to list all public repositories for the `bendystraw` GitHub user:

```bash
➜ uv run reporule list bendystraw
Getting public repos for bendystraw...
2025-04-30 21:53:06 [info     ] Repository report complete     count=2
             Public repositories in the bendystraw GitHub organization
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ name                        ┃ created_at ┃ archived ┃ fork  ┃ gh_id    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ beeradvocate-reviews-waffle │ 2015-04-05 │ False    │ True  │ 33453957 │
│ westernma-syrup             │ 2015-04-05 │ False    │ False │ 33454863 │
└─────────────────────────────┴────────────┴──────────┴───────┴──────────┘
```

## Ruleset command

This command applies a predefined GitHub branch ruleset to a single GitHub
repository of to all public repositories within a specific org or user.

```bash
➜ uv run reporule ruleset --help

 Usage: reporule ruleset [OPTIONS] ORG

 Apply a specified ruleset to a single repo or to all eligible
 repos that belong to a GitHub organization or user.
 The default ruleset applied is defined in data/default_branch_protections.json

 Rulesets will not be applied to archived repos, repos listed in
 repos_exceptions.yml, or repos that already have a ruleset of the same name.

 EXAMPLES:
 ----------
 reporule ruleset reichlab --all --dryrun
 reporule ruleset reichlab --repo reichlab.io
 reporule ruleset hubverse-io --all --ruleset hubverse_branch_protections

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    org      TEXT  GitHub organization or user name. [default: None] [required]                       │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────╮
│ --all                  Apply ruleset to all org/user repos not on the exception list. Cannot be used   │
│                        with --repo.                                                                    │
│ --repo           TEXT  GitHub repository name. Cannot be used with --all. [default: None]              │
│ --ruleset        TEXT  Ruleset filename to apply (without the .json extension). The file must be in    │
│                        the reporule/data directory.                                                    │
│                        [default: default_branch_protections]                                           │
│ --dryrun               Display repos to update without applying changes.                               │
│ --help                 Show this message and exit.                                                     │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Criteria for applying a branch

Before applying a branch ruleset to a repo, `reporule` will ensure that the
repo meets the following criteria:

- is not archived
- is not on the user/organization's "exception" list:
  [`data/repos_exception.yml`](https://github.com/reichlab/reporule/blob/main/src/reporule/data/repos_exception.yml)
- does not already have a ruleset with the same name

### Dryrun option

The `ruleset` command has a `--dryrun` option.

When this option is passed, `uv run reporule ruleset` will display the list of
repositories to be updated without applying any changes.

```bash
➜ uv run reporule ruleset bendystraw --all --dryrun
DRY RUN: Getting list of eligible repositories...

DRY RUN: would apply ruleset default-branch-protections to 2 repositories:
  • bendystraw/westernma-syrup
  • bendystraw/beeradvocate-reviews-waffle
```
