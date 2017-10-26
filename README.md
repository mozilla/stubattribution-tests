# stubattribution-tests
[![Build Status](https://travis-ci.org/mozilla/stubattribution-tests.svg?branch=master)](https://travis-ci.org/mozilla/stubattribution-tests)
[![updates](https://pyup.io/repos/github/mozilla/stubattribution-tests/shield.svg)](https://pyup.io/repos/github/mozilla/stubattribution-tests/)
[![Python 3](https://pyup.io/repos/github/mozilla/stubattribution-tests/python-3-shield.svg)](https://pyup.io/repos/github/mozilla/stubattribution-tests/)

Automated functional tests for the [!Stub Attribution service](https://github.com/mozilla-services/stubattribution).

Currently, this set of tests uses a real browser (Google Chrome), through [Sauce Labs](https://saucelabs.com/), with real end-user actions, and gets us all the way up to, **but not including** downloading/running/verifying the stub-installer build.
