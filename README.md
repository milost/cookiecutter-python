# Requirements

- Linux based system (... sorry for all Windows users)

# Use cookiecutter-python template

1. [Install cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/installation.html)

2. Create new project by running:

   ```bash
   cookiecutter gh:milost/cookiecutter-python
   ```

After `cookiecutter` has successfully set up the project, you can run `make` to get the [supported targets](#supported-targets) listed in detail below.

To setup an environment for the project execute:

1. `make install env=dev` or `make install` for installing without development dependencies.
2. After the successful installation of the environment it can be activated by running the target `make activate`.
3. Next since a repo is not set up ...do it
4. To use the following targets, you need to provide the corresponding tokens in the `.env` file:
   1. `make repo` - requires a [GITHUB_ACCESS_TOKEN](#configure-github-support)
   2. `make publish` - requires a [PYPI_TOKEN](#configure-pypi-support)
   3. `make docker-publish` - requires a [DOCKER_TOKEN](#configure-docker-support)
   4. `make test-publish` - requires a [CODECOV_TOKEN](#configure-codecov-support)

## Supported Targets

#### Setup targets

| Target                                  | Description                                                                                                       |
| --------------------------------------- | :---------------------------------------------------------------------------------------------------------------- |
| `install-pyenv`                         | Install [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) |
| `install [env=dev]`                     | Setup virtual environment and install project dependencies                                                        |
| `activate`                              | Activate the current project environment                                                                          |
| `flush-env`                             | Delete the virtual environment for this project                                                                   |
| `reinstall`                             | Deletes and recreates the virtual environment                                                                     |
| `repo [create-remote=true] [push=true]` | Create a git repository for the project                                                                           |

#### Development targets

| Target                               | Description                                                                   |
| ------------------------------------ | :---------------------------------------------------------------------------- |
| `run`                                | Execute `main` method of python project                                       |
| `lint`                               | Run linter ([flake8](https://flake8.pycqa.org/en/latest/)) over project files |
| `update`                             | Update project dependencies                                                   |
| `release [part=[major,minor,patch]]` | Increment package version                                                     |

#### Test targets

| Target                             | Description                                                             |
| ---------------------------------- | :---------------------------------------------------------------------- |
| `test [coverage=true] [show=true]` | Run tests quickly with the default Python                               |
| `test-upload`                      | Upload test results to online services ([codecov](https://codecov.io/)) |

#### Build targets

| Target    | Description                                                   |
| --------- | :------------------------------------------------------------ |
| `build`   | Build `sdist` and `wheel` distributions                       |
| `sdist`   | Build `sdist` distribution                                    |
| `wheel`   | Build `wheel` distribution                                    |
| `publish` | Build distribution using `build` target and upload it to PyPi |

#### Clean targets

| Target        | Description                                   |
| ------------- | :-------------------------------------------- |
| `clean`       | Clean _build_, _python_, and _test_ artifacts |
| `clean-build` | Clean _build_ artifacts                       |
| `clean-pyc`   | Clean _python_ artifacts                      |
| `clean-test`  | Clean _test_ artifacts                        |

#### Documentation targets

| Target             | Description                                            |
| ------------------ | :----------------------------------------------------- |
| `docs [show=true]` | Generate Sphinx HTML documentation, including API docs |
| `import-docs`      | Import the current project to ReadTheDocs              |

#### Docker targets

| Target           | Description                                  |
| ---------------- | :------------------------------------------- |
| `docker-image`   | Build docker image                           |
| `docker-rebuild` | Rebuild docker image                         |
| `docker-remove`  | Remove docker image                          |
| `docker-publish` | Push docker image to docker hub              |
| `docker-run`     | Execute the latest docker image              |
| `docker-service` | Run Docker image as a service                |
| `docker-shell`   | Run Docker image as service and attach to it |

## Configure PyPI support

The unique repository [upload token](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}/settings) is found on the settings page of your project.
You need write access to view this token.

## Configure CodeCov support

The unique repository [upload token](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}/settings) is found on the settings page of your project.
You need write access to view this token.

## Configure Docker support

To be able to push your image to docker hub you need an _access token_. Instructions on how to generate an access token can be found [here](https://docs.docker.com/docker-hub/access-tokens/). Once you have an access token, you can set the `DOCKER_TOKEN` environment variable in the `.env` file which is located in the projects root directory.

## Configure Documentation with ReadTheDocs

After the project has been created with `cookiecutter`, everything is already configured so that the documentation can be generated by [ReadTheDocs](https://readthedocs.org/). Once the repository has been is published on, say, GitHub, it can be imported into your ReadTheDocs account. To do this you can proceed as follows:

1. Login to ReadTheDocs using your GitHub account
2. Go to the [ReadTheDocs dashboard](https://readthedocs.org/dashboard/)
3. Click on [Import a project](https://readthedocs.org/dashboard/import/?)
4. Choose the project for which you want the generate the documentation (the `+` button next to the project name)
5. On the next page, simply press the `Next` button and your project will be imported into ReadTheDocs.

From now on ReadTheDocs will keep track and generate a new project documentation for every new release.

## Configure GitHub support

To be able to create a new GitHub repository for your project a personal access token is
needed to access your GitHub account. Instructions on how to create a personal access token
can be found [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).
Once the token has been created you can either set it as env variable yourself or set
the `GITHUB_ACCESS_TOKEN` variable in the `.env` file. After that you can use the `repo` target to create a repository on GitHub over the command line by exexcuing `make repo create-remote=true`. If you want to immediately push your initial project setup to GitHub use `make repo create-remote=true push=true`.
