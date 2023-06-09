# Peg Kmk

Whats kmk? Look at the original [README here](./OLDREADME.md)

## Soooo.... Why is this here?

Well there were a few things we at Boardsource wanted to do with kmk that were not best for the over all health of the project.
No hard feelings and we are still committing upstream as much as we can.
This fork is kept very in-sync with kmk/master

## Well then whats different?

1. This readme.
2. kmk folder is inside of /src
3. we build and distribute a .mpy version of kmk.
   we have a easy way to build .mpy versions simply run `docker compose up`.
4. we dont want your pr.
   Open your pr's in kmk and we will get them here.
5. Features Boardsource makes are added here first.

So really this is a known constant peg supports this version of kmk.
This is the version of kmk frozen into [bs-python](https://github.com/boardsource/bs-python)

## Fin.

In closing "Pay no attention to that man behind the curtain." You should not need to know about this but its here and there are reasons. please use, love and contribute to kmk its awesome and the people working on it are great.

## Getting Started
KMK requires [CircuitPython](https://circuitpython.org/) version 7.0 or higher.
Our getting started guide can be found
[here](/docs/en/Getting_Started.md).

## Code Style

KMK uses [Black](https://github.com/psf/black) with a Python 3.11 target and,
[(controversially?)](https://github.com/psf/black/issues/594) single quotes.
Further code styling is enforced with isort and flake8 with several plugins.
`make fix-isort fix-formatting` before a commit is a good idea, and CI will fail
if inbound code does not adhere to these formatting rules. Some exceptions are
found in `setup.cfg` loosening the rules in isolated cases, notably
`user_keymaps` (which is *also* not subject to Black formatting for reasons
documented in `pyproject.toml`).

## Tests

Unit tests within the `tests` folder mock various CircuitPython modules to allow
them to be executed in a desktop development environment.

Execute tests using the command `python -m unittest`.

## License, Copyright, and Legal

All software in this repository is licensed under the [GNU Public License,
version 3](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)).
All documentation and hardware designs are licensed under the [Creative Commons
Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
license. Contributions to this repository must use these licenses unless
otherwise agreed to by the Core team.

**Due to ethical and legal concerns, any works derived from GitHub Copilot or
similar artificial intelligence tooling are unacceptable for inclusion in any
first-party KMK repository or other code collection. We further recommend not
using GitHub Copilot while developing anything KMK-related, regardless of
intent to submit upstream.**
