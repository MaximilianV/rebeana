FROM maximilianvoelker/pm4py

RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    #
    # Install pylint
    && pip --disable-pip-version-check --no-cache-dir install pylint \
    && pip --disable-pip-version-check --no-cache-dir install autopep8 \
    && pip --disable-pip-version-check --no-cache-dir install rope \
    && pip --disable-pip-version-check --no-cache-dir install toml \
    && pip --disable-pip-version-check --no-cache-dir install statsmodels \
    && pip --disable-pip-version-check --no-cache-dir install seaborn \
    && pip --disable-pip-version-check --no-cache-dir install questionary \
    #
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog
