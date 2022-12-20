# Best practices

## README.md

1. Use [Markdown lint](https://dlaa.me/markdownlint/) to adhere to
    [Markdown rules](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md).

## Dockerfile

1. Use best practices:
    1. Docker's [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/).
    1. Project Atomic's [Container Best practices](http://docs.projectatomic.io/container-best-practices).
1. Use "lint" when applicable.
    1. Online linter: [FROM: latest](https://www.fromlatest.io)
    1. GitHub [projectatomic/dockerfile_lint](https://github.com/projectatomic/dockerfile_lint) using Docker

        ```console
        sudo docker run -it \
          --rm \
          --privileged \
          --volume $PWD:/root/ \
          projectatomic/dockerfile-lint \
            dockerfile_lint -f Dockerfile
        ```

    1. **Note:** Linters may erroneously report "ARG before FROM" which is supported as of
        Enterprise Edition [17.06.01](https://docs.docker.com/engine/release-notes/#17061-ee-1) and
        Community Edition [17.05.0](https://docs.docker.com/engine/release-notes/#17050-ce).

## Makefile

1. Modifications:
    1. Change following value to appropriate Docker tag.

        ```make
        DOCKER_IMAGE_NAME := senzing/template
        ```

1. Use `make docker-build-base` occasionally to populate the docker image cache with layers that change infrequently.
1. Once a "base" has been created, use `make docker-build` to build during development and make final builds.

## CONTRIBUTING.md

1. Modifications:
    1. Change following value to appropriate Git repository name.

        ```markdown
        export GIT_REPOSITORY=template-docker
        ```
