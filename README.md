# Tests for Stub Attribution

This repository contains tests for Firefox
[Stub Attribution](https://github.com/mozilla-services/stubattribution) - A
service which accepts an attribution code and returns a modified stub
installer.

[![license](https://img.shields.io/badge/license-MPL%202.0-blue.svg)](https://github.com/mozilla/stubattribution-tests/blob/master/LICENSE.txt)
[![travis](https://img.shields.io/travis/mozilla/stubattribution-tests.svg?label=travis)](http://travis-ci.org/mozilla/stubattribution-tests/)
[![updates](https://pyup.io/repos/github/mozilla/stubattribution-tests/shield.svg)](https://pyup.io/repos/github/mozilla/stubattribution-tests/)
[![Python 3](https://pyup.io/repos/github/mozilla/stubattribution-tests/python-3-shield.svg)](https://pyup.io/repos/github/mozilla/stubattribution-tests/)

## Table of contents:

* [Getting involved](#getting-involved)
* [How to run the tests](#how-to-run-the-tests)
* [Writing tests](#writing-tests)
* [Test plan](#test-plan)

## Getting involved

We love working with contributors to improve test coverage on our projects, but it
does require a few skills. By contributing to our test suite you will have an
opportunity to learn and/or improve your skills with Python, Selenium
WebDriver, GitHub, virtual environments, the Page Object Model, and more.

Our [new contributor guide][guide] should help you to get started, and will
also point you in the right direction if you need to ask questions.

## How to run the tests

This suite of tests uses a real browser (Google Chrome) on Windows 10, with
real end-user actions, and gets us all the way up to, **but not including**
downloading/running/verifying the stub-installer build.

### Clone the repository

If you have cloned this project already, then you can skip this; otherwise
you'll need to clone this repo using Git. If you do not know how to clone a
GitHub repository, check out this [help page][git clone] from GitHub.

If you think you would like to contribute to the tests by writing or
maintaining them in the future, it would be a good idea to create a fork of
this repository first, and then clone that. GitHub also has great instructions
for [forking a repository][git fork].

### Run the tests using Sauce Labs

You will need a [Sauce Labs][] account, with a `.saucelabs` file in your home
directory containing your username and API key, as follows:

```ini
[credentials]
username = username
key = secret
```

Then you can run the tests using [Docker][]. The `--mount` argument is
important, as it allows your `.saucelabs` file to be accessed by the Docker container:

```
$ docker build -t stubattribution-tests .
$ docker run -it --mount type=bind,source=$HOME/.saucelabs,destination=/src/.saucelabs,readonly stubattribution-tests
```

### Run the tests using Google Chrome on Windows

Whilst we recommend using Sauce Labs to run the tests, it's also possible to
run them locally if you have Windows 10, [Google Chrome][], and
[chromedriver][].

Install [Pipenv][], and then run the following command:

```
$ pipenv run pytest
```

## Writing tests

If you want to get involved and add more tests, then there are just a few
things we'd like to ask you to do:

1. Follow our simple [style guide][].
2. Fork this project with your own GitHub account.
3. Make sure all tests are passing, and submit a pull request.
4. Always feel free to reach out to us and ask questions.

## Test plan

The current test plan can be found on the [Mozilla wiki][]. Test suites that
require manual execution are stored in our [Testrail instance][].

[guide]: http://firefox-test-engineering.readthedocs.io/en/latest/guide/index.html
[git clone]: https://help.github.com/articles/cloning-a-repository/
[git fork]: https://help.github.com/articles/fork-a-repo/
[sauce labs]: https://saucelabs.com/
[docker]: http://docker.com/
[google chrome]: https://www.google.com/chrome/
[chromedriver]: https://sites.google.com/a/chromium.org/chromedriver/
[pipenv]: https://docs.pipenv.org/
[style guide]: https://wiki.mozilla.org/QA/Execution/Web_Testing/Docs/Automation/StyleGuide
[Mozilla wiki]: https://wiki.mozilla.org/Firefox/Stub_Attribution/Test_Plan
[Testrail instance]: https://testrail.stage.mozaws.net/index.php?/projects/overview/42
