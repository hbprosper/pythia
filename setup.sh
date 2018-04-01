#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PATH=$DIR/bin:$PATH
export PYTHIA8=$EXTERNAL
export PYTHIA8DATA=`pythia8-config`
export LD_LIBRARY_PATH=$PYTHIA8/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$PYTHIA8/lib:$DYLD_LIBRARY_PATH
export LHAPDF_DATA_PATH=$EXTERNAL/share/LHAPDF/PDFsets
export PYTHONPATH=$DIR/python:$PYTHONPATH
