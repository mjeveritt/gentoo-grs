#!/bin/bash -e

source /etc/profile
env-update
emerge -b1q portage
emerge -b1q argp-standalone
emerge -b1q app-portage/grs

emerge -b1q binutils
emerge -b1q gcc
emerge -b1q musl

# This is from the tarball.
rm -rf /etc/portage/package.use

install-worldconf
emerge -bevq --keep-going --verbose-conflicts --with-bdeps=y @world
clean-worldconf
