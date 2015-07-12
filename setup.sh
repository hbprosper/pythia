#!/bin/bash
export PATH=$PWD/bin:$PATH
export PYTHIA8=$EXTERNAL
export PYTHIA8DATA=`pythia8-config`
export DYLD_LIBRARY_PATH=$PYTHIA8/lib
export PYTHONPATH=$PWD/python:$PYTHONPATH
