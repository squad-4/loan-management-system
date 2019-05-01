# Loan Management System

> A simple API to manage loan payments for a fintech

[![Build Status](https://travis-ci.org/squad-4/loan-management-system.svg?branch=master)](https://travis-ci.org/squad-4/loan-management-system) [![codecov](https://codecov.io/gh/squad-4/loan-management-system/branch/master/graph/badge.svg)](https://codecov.io/gh/squad-4/loan-management-system) [![Updates](https://pyup.io/repos/github/squad-4/loan-management-system/shield.svg)](https://pyup.io/repos/github/squad-4/loan-management-system/) [![Python 3](https://pyup.io/repos/github/squad-4/loan-management-system/python-3-shield.svg)](https://pyup.io/repos/github/squad-4/loan-management-system/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![License](https://img.shields.io/github/license/squad-4/loan-management-system.svg)](https://opensource.org/licenses/GPL-3.0)

## Features

- Loan management
- Payments control
- Outstanding balance

## Development

The following guidelines will help you to have a copy ready and running of the project so you can play around, make changes and improvements.

### Installing and Running

The application was built using **Django** framework with **Django-Rest** framework extension. It shares the same basic characteristics and requirements any other Python software based on Django.

#### Requirements

- [Python 3](http://python.org/)
- [Pip](https://pip.pypa.io/)
- [Django](http://djangoproject.com/)
- [Django-Rest](https://www.django-rest-framework.org)
- [SQLite](http://sqlite.org/) (or any other supported database)

These are optional but recommended.

- [Black](http://black.readthedocs.io/)
- [Codecov](http://codecov.io/)
- [Flake8](http://flake8.pycqa.org/)
- [Pipenv](http://pipenv.readthedocs.io)
- [Pre-commit](http://pre-commit.com/)

#### Installing

First, you need a copy of the source code, you can download it (here)[https://github.com/squad-4/loan-management-system] or clone the project. To clone the project you need [Git](https://git-scm.com), if you don't have it installed go to the official site and follow the instructions, if you already have it just open a terminal application and enter the following commands.

```shell
$ cd desired/path/
$ git clone https://github.com/squad-4/loan-management-system
```

The next step is install the project's Python dependencies. Just like _Git_ if you still don't have it go to the [official site](http://python.org/) and get it done. You'll also need [Pip](https://pip.pypa.io/), same rules applys here. Another interesting tool that is not required but strongly recommended is [Pipenv](http://pipenv.readthedocs.io), it helps to manage dependencies and virtual envinronments.

Installing with **Pip**:

```shell
$ cd path/to/loan-project
$ pip install --upgrade django djangorestframework  # and any other optional packages
```

Installing with **Pipenv**:

```shell
$ pip install --upgrade pipenv
$ cd path/to/loan-project
$ pipenv sync -d
```

Finally, configure the application. This will require you to define a few variables and create the database.

**Note 1** - If you are using Pipenv you need to start a shell loading the apps virtual environment before run any Python command. Just enter the following.

```shell
$ pipenv shell
```

**Note 2** - By default Django applications uses SQLite, but you can use any other supported database, take a look [here](https://docs.djangoproject.com) to choose one. For the purpose of this example we will use the default (SQLite) and assuming it's already installed.

```shell
$ python manage.py migrate
```

#### Running

Django has a development server to make it easy run applications for testing and debug.

```shell
$ python manage.py runserver
```

That's it!

### Contributing

If you intend to contribute, instead of just making a copy from the original repository you have to fork the project on [GitHub](https://github.com/squad-4/loan-management-system) into your own account, then clone from the fork and send pull requests with your changes.

Two of the optional dependencies become mandatory, **Black** and **Pre-commit**, you need to install them in order to validate the coding style adopted by the project. If you are using Pipenv you may already have them, otherwise run `pip install --upgrade black pre-commit`.

Install Pre-commit rules.

```shell
$ cd path/to/loan-project
$ pre-commit install  # remember to load a shell first if using Pipenv
```

## About

This project is part of the final challenge for the **Acelera DEV - Python para Web** program promoted by [Codenation](https://codenation.dev) running between april and may of 2019.

## Authors

- [Caio Torresi](https://github.com/caioCT)
- [Eric Dantas](https://github.com/ericrommel)
- [Felipe Pimenta](https://github.com/fhpimenta)
- [Juliano Fernandes](https://github.com/julianolf)
- [William Galleti](https://github.com/wgalleti)

## License

This project is licensed under the GNU License - see the [License](./LICENSE) file for details.
