#!/usr/bin/env python
#-----------------------------------------------------------------------------
# File: pythiaRun.py
#-----------------------------------------------------------------------------
import os, sys
import pythia8 as p8
import pyHepMC3 as hp
# linked HepMC3/python/test to lib/python3.9/site-packages
from Pythia8ToHepMC3 import Pythia8ToHepMC3
#-----------------------------------------------------------------------------
WriterAscii = hp.HepMC3.WriterAscii
ReaderAscii = hp.HepMC3.ReaderAscii
GenEvent    = hp.HepMC3.GenEvent
Units       = hp.HepMC3.Units
Print       = hp.HepMC3.Print
#-----------------------------------------------------------------------------
def get_filenames():
    argv = sys.argv[1:]
    argc = len(argv)
    if argc < 1:
        sys.exit('''
        Usage:
        02_study.py control-file-name
        ''')
    inpfilename = argv[0]
    if not os.path.exists(inpfilename):
        sys.exit('''
        file %s NOT found!
        ''' % inpfilename)
    outfilename = inpfilename.replace('.txt', '.hepmc3')

    print('control file: %s' % inpfilename)
    print('output  file: %s' % outfilename)
    
    return inpfilename, outfilename
#-----------------------------------------------------------------------------
def main():
    
    inpfilename, outfilename = get_filenames()

    toHepMC3 = Pythia8ToHepMC3()
    writer   = WriterAscii(outfilename)

    # Read Pythia instructions from control file
    pythia   = p8.Pythia()
    pythia.readFile(inpfilename)

    nEvent   = pythia.mode("Main:numberOfEvents")
    nAbort   = pythia.mode("Main:timesAllowErrors")

    print("number of events to generate         %d" % nEvent)
    print("maximum number of events bad events  %d" % nAbort)
    
    # Initialize Pythia
    pythia.init()

    Abort = 0
    for event_number in range(nEvent):

        # generate event
        if pythia.next():

            # write ouut event in HepMC3 format
            hepmcevt = GenEvent()
            toHepMC3.fill_next_event1(pythia, hepmcevt, event_number)
            writer.write_event(hepmcevt)
            
        else:
            # we could be reading from an LHE file, so check
            # for end of file.
            if pythia.info.atEndOfFile():
                print("** reached end of LHE file")
                break
            
            Abort += 1
            if Abort < nAbort:
                print("** abort event")
                break

    pythia.stat()
#-----------------------------------------------------------------------------
try:
    main()
except KeyboardInterrupt:
    print('\nbye!')
    

