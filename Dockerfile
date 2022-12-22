ARG BASE_IMAGE=senzing/senzingapi-runtime 
FROM ${BASE_IMAGE}

ENV REFRESHED_AT=2022-12-21

LABEL Name="senzing/code-snippets" \
      Maintainer="support@senzing.com" \
      Version="0.0.1"

# Run as "root" for system installation.

USER root

# Install packages via apt.

RUN apt-get update \
 && apt-get -y install \
      vim \
      nano \
      curl \
      less \
      python3 \
      ipython3 \
      python3-pip \
      python3-virtualenv \
      python3-venv \
 && rm -rf /var/lib/apt/lists/*

## Copy files from repository.

COPY ./Python/ /code-snippets/Python
COPY ./Resources/ /code-snippets/Resources
COPY ./rootfs /

# Make non-root container.

USER 1001

# Runtime environment variables.

ENV LD_LIBRARY_PATH=/opt/senzing/g2/lib:/opt/senzing/g2/lib/debian
ENV PATH=${PATH}:/opt/senzing/g2/python
ENV PYTHONPATH=/opt/senzing/g2/sdk/python
ENV PYTHONUNBUFFERED=1
ENV SENZING_DOCKER_LAUNCHED=true

WORKDIR /code-snippets
ENTRYPOINT ["/bin/bash"]
