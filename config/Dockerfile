FROM registry.fedoraproject.org/fedora-minimal:33

ARG DEVEL=""
ARG VERSION=0.1.0
ARG PATTERNFLY_VERSION=3.59.5
ARG PATTERNFLY_BOOTSTRAP_VERSION=3.3.7

ENV NAME="Faros Config UI" \
    DEVEL="$DEVEL" \
    VERSION="$VERSION" \
    PATTERNFLY_VERSION="$PATTERNFLY_VERSION" \
    PATTERNFLY_BOOTSTRAP_VERSION="$PATTERNFLY_BOOTSTRAP_VERSION" \
    ARCH=x86_64 \
    SUMMARY="Project Faros configuration web application" \
    DESCRIPTION="A simple Flask application designed to provide an intuitive \
                 user interface for generating Project Faros YML configuration \
                 files, for provisioning OpenShift Container Platform, \
                 OpenShift Container Storage, and Open Data Hub onto edge \
                 computing hardware."

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      name="$FGC/$NAME" \
      version="$VERSION" \
      is_devel="$DEVEL" \
      maintainer="James Harmison (jharmison@redhat.com)"

# Prereqs
RUN INSTALL_PKGS="python3 python3-setuptools python3-pip" && \
    microdnf update && \
    microdnf install $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    microdnf clean all && \
    mkdir -p /pre

# Application files
COPY entrypoint.py /usr/local/bin/entrypoint.py
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY faros_config_ui /app
COPY faros_config /pre/faros_config

# Application installation
RUN pip3 install --no-cache-dir /pre/faros_config && \
    rm -rf /pre && \
    echo "$VERSION" > /app/VERSION.txt && \
    curl -Lo /app/faros_config_ui/static/js/bootstrap.js \
        https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/$PATTERNFLY_BOOTSTRAP_VERSION/js/bootstrap.min.js && \
    curl -Lo /app/faros_config_ui/static/js/patternfly.js \
        https://cdnjs.cloudflare.com/ajax/libs/patternfly/$PATTERNFLY_VERSION/js/patternfly.min.js && \
    curl -Lo /app/faros_config_ui/static/css/patternfly.css \
        https://cdnjs.cloudflare.com/ajax/libs/patternfly/$PATTERNFLY_VERSION/css/patternfly.min.css && \
    curl -Lo /app/faros_config_ui/static/css/patternfly-additions.css \
        https://cdnjs.cloudflare.com/ajax/libs/patternfly/$PATTERNFLY_VERSION/css/patternfly-additions.min.css && \
    [ "$DEVEL" ] && pip3 install -e /app || pip3 install --no-cache-dir /app

USER 1001
EXPOSE 5000

CMD /usr/local/bin/entrypoint.sh
