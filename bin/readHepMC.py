#!/usr/bin/env python
# -----------------------------------------------------------------------
#     status = +- (10 * i + j)
#     + : still remaining particles
#     - : decayed/branched/fragmented/... and not remaining
#     i = 1 - 9 : stage of event generation inside PYTHIA
#     i = 10 -19 : reserved for future expansion
#     i >= 20 : free for add-on programs
#     j = 1 - 9 : further specification

# In detail, the list of used or foreseen status codes is:

#     11 - 19 : beam particles
#         11 : the event as a whole
#         12 : incoming beam
#         13 : incoming beam-inside-beam (e.g. gamma inside e)
#         14 : outgoing elastically scattered
#         15 : outgoing diffractively scattered
#     21 - 29 : particles of the hardest subprocess
#         21 : incoming
#         22 : intermediate (intended to have preserved mass)
#         23 : outgoing
#         24 : outgoing, nonperturbatively kicked out in diffraction
# -----------------------------------------------------------------------
import os, sys
from string import split, strip, atoi, atof
from ROOT import *
# -----------------------------------------------------------------------
print
print "==> compiling pdg.cc"
gROOT.ProcessLine(".L pdg.cc+")

class Event:
    def __init__(self):
        pass
    def __del__(self):
        pass

class Particle:
    def __init__(self):
        self.event = None
        self.pid = 0
        self.status = 0
        self.vertex = 0
        self.energy = 0.0
        self.px     = 0.0
        self.py     = 0.0
        self.pz     = 0.0
        self.mass   = 0.0

    def __del__(self):
        pass

    def __str__(self):
        d = ''
        if self.event.vertex.has_key(self.vertex):
            v = self.event.vertex[self.vertex]
            if len(v) == 1:
                d = '%d' % v[0]
            elif len(v) > 1:
                d = '%d %d' % (v[0], v[-1])
        rec = '%-10s %6d %3d (%6.1f, %6.1f, %6.1f, %6.1f)   (%s)' \
          % (pdg.particleName(self.pid),
             self.pid,
             self.status,
             self.energy,
             self.px,
             self.py,
             self.pz,
             d)
        return rec
# -----------------------------------------------------------------------    
def readEvent(inp, nvertices=-1):
    # find start of event
    token = None
    while 1:
        token = split(inp.readline())
        key = token[0]
        if key != 'E': continue
        #print 'Found event'
        break

    if token == None:
        print "** can't find start of event"
        sys.exit(0)

    event = Event()
    event.eventNumber = atoi(token[1])
    event.nMP         = atoi(token[2])
    event.processID   = atoi(token[6])
    event.nvertices   = atoi(token[8])
    event.barcode1    = atoi(token[9])
    event.barcode2    = atoi(token[10])
    #print "\tbarcode 1: %d" % event.barcode1
    #print "\tbarcode 2: %d" % event.barcode2
    
    if nvertices < 0: nvertices = event.nvertices
    maxvertices = min(nvertices, event.nvertices)
    
    event.particle = {}
    event.vertex   = {}
    vertex   = event.vertex
    particle = event.particle
    while 1:
        token = split(inp.readline())
        key = token[0]
        if key == 'F':
            event.parton1  = atoi(token[1])
            event.parton2  = atoi(token[2])
            event.x1  = atof(token[3])
            event.x2  = atof(token[4])
            event.Q2  = atof(token[5])
            #print '\tfound PDF info'
            
        elif key == 'V':
            barcode = atoi(token[1])
            vertex[barcode] = []
            nout = atoi(token[8])
            #print '\tvertex %d' % barcode
            
            for ii in xrange(nout):
                record = inp.readline()
                token = split(record)
                key = token[0]
                if key != 'P':
                    print "*** error *** something wrong with event record"
                    print record
                    sys.exit(0)
                code = atoi(token[1])
                vertex[barcode].append(code)
                
                particle[code] = Particle()
                particle[code].pid = atoi(token[2])
                particle[code].px = atof(token[3])
                particle[code].py = atof(token[4])
                particle[code].pz = atof(token[5])
                particle[code].energy = atof(token[6])
                particle[code].mass   = atof(token[7])
                particle[code].status = atoi(token[8])
                particle[code].vertex = atoi(token[11])
                particle[code].event  = event
        if len(vertex) >= maxvertices:
            break
    return event
# -----------------------------------------------------------------------
def hardScatter(event):
    hevent = Event()
    hevent.eventNumber = event.eventNumber
    hevent.nMP         = event.nMP
    hevent.processID   = event.processID
    hevent.nvertices   = 0
    hevent.barcode1    = event.barcode1
    hevent.barcode2    = event.barcode2
    hevent.parton1     = event.parton1
    hevent.parton2     = event.parton2
    hevent.x1  = event.x1
    hevent.x2  = event.x2
    hevent.Q2  = event.Q2
    hevent.particle = {}
    hevent.vertex   = {}
    
    vertex   = event.vertex
    particle = event.particle    
    codes    = particle.keys()
    codes.sort()
    for code in codes:
        status = abs(particle[code].status)
        if status < 21: continue
        if status > 29: continue

        vtx = particle[code].vertex
        pid = particle[code].pid
        if vertex.has_key(vtx):
            d = vertex[vtx][0]
            count = 0
            while particle[d].pid == pid and count < 100:
                count += 1
                vtx = particle[d].vertex
                if not vertex.has_key(vtx): break
                d = vertex[vtx][0]
            particle[code].vertex = vtx

        #print "%4d\t%s" % (code, particle[code])
        hevent.particle[code] = particle[code]
        if vertex.has_key(vtx):
            hevent.vertex[vtx] = vertex[vtx]
        else:
            hevent.vertex[vtx] = []

        if not abs(pid) in [15, 23, 24, 25]: continue
         
        # loop over daughters
        for dcode in hevent.vertex[vtx]:
            vtx = particle[dcode].vertex
            pid = particle[dcode].pid
            if vertex.has_key(vtx):
                d = vertex[vtx][0]
                count = 0
                while particle[d].pid == pid and count < 100:
                    count += 1
                    vtx = particle[d].vertex
                    if not vertex.has_key(vtx): break
                    d = vertex[vtx][0]
                particle[dcode].vertex = vtx

            #print "%4d\t%s" % (code, particle[code])
            hevent.particle[dcode] = particle[dcode]
            if vertex.has_key(vtx):
                hevent.vertex[vtx] = vertex[vtx]
            else:
                hevent.vertex[vtx] = []

            if abs(particle[dcode].pid) != 15: continue
            
            for ccode in hevent.vertex[vtx]:
                vtx = particle[ccode].vertex
                pid = particle[ccode].pid
                if vertex.has_key(vtx):
                    d = vertex[vtx][0]
                    count = 0
                    while particle[d].pid == pid and count < 100:
                        count += 1
                        vtx = particle[d].vertex
                        if not vertex.has_key(vtx): break
                        d = vertex[vtx][0]
                    particle[ccode].vertex = vtx

                #print "%4d\t%s" % (code, particle[code])
                hevent.particle[ccode] = particle[ccode]
                if vertex.has_key(vtx):
                    hevent.vertex[vtx] = vertex[vtx]
                else:
                    hevent.vertex[vtx] = []
                       
    hevent.nvertices = len(hevent.vertex)
    return hevent
# -----------------------------------------------------------------------    
def printTable(event):
    vertex   = event.vertex
    particle = event.particle    
    codes    = particle.keys()
    codes.sort()
    for code in codes:
        print "%4d\t%s" % (code, particle[code])
# -----------------------------------------------------------------------            
def printTree(event, barcode=None, depth=0):
    particle = event.particle
    vertex = event.vertex
    
    if depth == 0:
        codes    = particle.keys()
        codes.sort()
        barcode = codes[0]
        p = particle[barcode]
        print p
        barcode = codes[1]            

    elif depth > 5:
        return

    p = particle[barcode]
    strg = "..."*depth    
    strg += '%s' % p
    print strg

    depth += 1
    daughters = vertex[p.vertex]
    if len(daughters) == 0: return
    for code in daughters:
        if particle.has_key(code):
            printTree(event, code, depth)
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------    
def main():
    argv = sys.argv[1:]
    argc = len(argv)
    if argc < 1:
        print '''
    Usage:
        ./readHepMC.py <HepMC-file-name>
        '''
        sys.exit(0)

    print "="*80
    print "\t\t\tread HepMC file"
    print "="*80
    filename = argv[0]
    if not os.path.exists(filename):
        print "** can't open file %s" % filename
        sys.exit(0)

    try:
        nevents = atoi(os.popen('grep "^E " %s | wc -l' % filename).read())
    except:
        print "** can't get number of events"
        sys.exit(0)

    # ------------------------------------------------------------
    print "number of events in file: %d" % nevents
    
    inp = open(filename)
    version = None
    while 1:
        version = strip(inp.readline())
        if version == '': continue
        token = split(version)
        if token[0] == 'HepMC::Version':
            version = token[1]
            break
        
    print "HepMC version: %s" % version
    inp.readline() # skip start of listing

    # loop over events
    for entry in xrange(nevents):
        event  = readEvent(inp)
        hevent = hardScatter(event)
        
        print "\n===> Event: %d" % entry
        #printTable(hevent)
        printTree(hevent)
        
# -----------------------------------------------------------------------
main()

    
