#!/bin/bash
export PATH=$PWD/bin:$PATH
export PYTHIA8=$EXTERNAL
export PYTHIA8DATA=`pythia8-config`
export LD_LIBRARY_PATH=$PYTHIA8/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$PWD/python:$PYTHONPATH
