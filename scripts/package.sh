#!/usr/bin/env bash

tar -C $HOME -c --exclude-vcs -j -v -f "fvwmcfg.tar.bz2" .fvwm/
