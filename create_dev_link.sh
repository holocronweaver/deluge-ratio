#! /usr/bin/env bash
# Must be called from project root directory.
mkdir temp
export PYTHONPATH=./temp
/usr/bin/python2 setup.py build develop --install-dir ./temp
cp ./temp/Ratio.egg-link $HOME/.config/deluge/plugins
rm -fr ./temp
