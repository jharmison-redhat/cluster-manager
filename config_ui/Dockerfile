FROM registry.fedoraproject.org/fedora-minimal:33

ARG DEVEL=""

ENV NAME="Faros Config UI" \
    DEVEL="$DEVEL" \
    VERSION=0.1.0 \
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

RUN INSTALL_PKGS="python3 python3-setuptools python3-pip" && \
    microdnf update && \
    microdnf install $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    microdnf clean all

COPY entrypoint.py /usr/local/bin/entrypoint.py
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY app /app

RUN echo "$VERSION" > /app/VERSION.txt && \
    [ "$DEVEL" ] && pip3 install -e /app || pip3 install --no-cache-dir /app

USER 1001
EXPOSE 5000

CMD /usr/local/bin/entrypoint.sh
