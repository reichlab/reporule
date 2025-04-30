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

This command lists all public repositories associated with a specific GitHub user or organization. We used a
version of this in the past when auditing repositories in the `reichlab` GitHub org to review potential project
to archive, for example.

```bash
➜ uv run reporule list --help

 Usage: reporule list [OPTIONS] ORG

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────╮
│ *    org      TEXT  [default: None] [required]                                            │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
```

For example, to list all public repositories in the `hubverse-org` GitHub organization:

```bash
➜ uv run reporule list hubverse-org
Getting public repos for hubverse-org...
2025-04-30 13:40:44 [info     ] Repository report complete     count=42
                    Repositories in the hubverse-org GitHub organization
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ name                          ┃ created_at           ┃ archived ┃ visibility ┃ id        ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ hubUtils                      │ 2022-10-03T08:19:38Z │ False    │ public     │ 544788632 │
│ hubDocs                       │ 2022-10-12T19:53:48Z │ False    │ public     │ 550456045 │
│ hubTemplate                   │ 2022-10-20T17:01:34Z │ False    │ public     │ 554938992 │
│ example-complex-scenario-hub  │ 2022-11-10T14:45:53Z │ False    │ public     │ 564357442 │
│ example-simple-forecast-hub   │ 2022-11-10T14:50:39Z │ False    │ public     │ 564359467 │
│ schemas                       │ 2022-11-10T15:10:55Z │ False    │ public     │ 564368300 │
│ example-complex-forecast-hub  │ 2022-11-16T15:35:28Z │ False    │ public     │ 566869759 │
│ hubEnsembles                  │ 2022-12-21T13:54:53Z │ False    │ public     │ 580806880 │
│ hubValidations                │ 2023-04-19T10:36:09Z │ False    │ public     │ 629940060 │
│ hubVis                        │ 2023-07-03T15:07:33Z │ False    │ public     │ 661753342 │
│ .github                       │ 2023-07-20T09:44:56Z │ False    │ public     │ 668649904 │
│ ci-testhub-simple             │ 2023-09-18T12:50:44Z │ False    │ public     │ 693146396 │
│ hubverse-actions              │ 2023-09-20T08:40:27Z │ False    │ public     │ 694055638 │
│ hubCI                         │ 2023-09-20T09:53:12Z │ False    │ public     │ 694085080 │
│ hubEvals                      │ 2024-01-17T15:08:26Z │ False    │ public     │ 744567759 │
│ hubverse-developer-actions    │ 2024-01-19T13:22:44Z │ False    │ public     │ 745499953 │
│ hubDevs                       │ 2024-01-19T14:33:40Z │ False    │ public     │ 745529025 │
│ hubStyle                      │ 2024-01-22T13:40:05Z │ False    │ public     │ 746692236 │
│ hubverse-cloud                │ 2024-01-29T18:19:00Z │ False    │ public     │ 749961935 │
│ hubEnsemblesManuscript        │ 2024-02-12T15:59:41Z │ False    │ public     │ 756408646 │
│ hubverse-infrastructure       │ 2024-02-13T17:03:46Z │ False    │ public     │ 756974843 │
│ hubData                       │ 2024-02-26T10:31:23Z │ False    │ public     │ 763457042 │
│ hubAdmin                      │ 2024-02-26T10:43:49Z │ False    │ public     │ 763462315 │
│ hubExamples                   │ 2024-03-13T19:14:09Z │ False    │ public     │ 771692906 │
│ flusight_hub_archive          │ 2024-04-03T12:56:37Z │ False    │ public     │ 781472007 │
│ hubverse-transform            │ 2024-04-09T19:14:35Z │ False    │ public     │ 784398483 │
│ hubverse                      │ 2024-06-06T19:42:44Z │ False    │ public     │ 811537557 │
│ ci-testhub-simple-old-orgname │ 2024-06-17T14:23:44Z │ False    │ public     │ 816332373 │
│ hubverse-org.r-universe.dev   │ 2024-07-18T13:09:27Z │ False    │ public     │ 830533843 │
│ hub-dashboard-predtimechart   │ 2024-08-19T14:48:55Z │ False    │ public     │ 844581621 │
│ hubDataPy                     │ 2024-08-19T16:03:01Z │ True     │ public     │ 844612645 │
│ pkg-health-check              │ 2024-09-25T21:36:22Z │ False    │ public     │ 863185759 │
│ hub-dash-site-builder         │ 2024-10-24T22:25:13Z │ False    │ public     │ 878172183 │
│ hub-dashboard-control-room    │ 2024-10-24T22:26:54Z │ False    │ public     │ 878172677 │
│ hub-dashboard-template        │ 2024-10-29T17:54:33Z │ False    │ public     │ 880429531 │
│ hubPredEvalsData              │ 2024-12-17T17:03:55Z │ False    │ public     │ 904848847 │
│ test-docker-hubValidations    │ 2025-01-03T00:51:58Z │ False    │ public     │ 911413799 │
│ predevals                     │ 2025-01-13T17:09:28Z │ False    │ public     │ 916215399 │
│ test-docker-hubUtils-dev      │ 2025-01-14T19:33:03Z │ False    │ public     │ 916801091 │
│ hubPredEvalsData-docker       │ 2025-01-14T23:47:46Z │ False    │ public     │ 916882091 │
│ hub-data                      │ 2025-04-02T16:52:02Z │ False    │ public     │ 959354605 │
│ hubverse-site                 │ 2025-04-08T19:00:41Z │ False    │ public     │ 962845497 │
└───────────────────────────────┴──────────────────────┴──────────┴────────────┴───────────┘
```

## Ruleset command

This command applies a predefined GitHub branch ruleset to:

- single GitHub repository:

    ```bash
    uv run reporule ruleset bsweger --repo cladetime
    ```

- OR to all public repositories associated with a specific org or user:

   ```bash
   uv run reporule ruleset hubverse-org --all
   ```

Before applying the ruleset to a repo, the command will ensure it meets the following criteria:

- is not archived
- is not on the user/organization's "exception" list:
  [`data/repos_exception.yml`](https://github.com/reichlab/reporule/blob/main/src/reporule/data/repos_exception.yml)
- does not already have a ruleset with the same name

> [!TIP]
> The `ruleset` command has a `--dryrun` option, which will display the impacted repositories without
> updating any of their rulesets.
