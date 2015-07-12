// main42.cc is a part of the PYTHIA event generator.
// Copyright (C) 2013 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// It illustrates how Les Houches Event File input can be used in PYTHIA
// and events written to HepMC format


#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/HepMC2.h"
#include "HepMC/GenEvent.h"   
#include "HepMC/IO_GenEvent.h"

using namespace Pythia8; 
using namespace std;

int main(int argc, char* argv[]) {

  // Check that correct number of command-line arguments
  if (argc < 2) {
    cerr << " Unexpected number of command-line arguments." << endl
         << " Usage:" << endl
         << "    pythiaRun <card-file> <output-HepMCfile>" << endl;
    return 1;
  }

  // Check that the provided input name corresponds to an existing file.
  ifstream is(argv[1]);  
  if (!is) {
    cerr << " Command-line file " << argv[1] << " was not found. \n"
         << " Program stopped! " << endl;
    return 1;
  }
  // Confirm that external files will be used for input and output.
  cout << "\n >>> PYTHIA settings will be read from file " << argv[1] << endl;


  string HepMCfile(".HepMCfile");
  if (argc > 2)
    {
      HepMCfile = string(argv[2]);
    cout  << " HepMC events will be written to file " 
	  << HepMCfile << " <<< \n" << endl;
    }

  // Interface for conversion from Pythia8::Event to HepMC event. 
  HepMC::Pythia8ToHepMC ToHepMC;
  // Specify file where HepMC events will be stored.
  HepMC::IO_GenEvent ascii_io(HepMCfile.c_str(), std::ios::out);
 
  // Generator. 
  Pythia pythia;

  // Read in commands from external file.
  pythia.readFile(argv[1]);    

  // Extract settings to be used in the main program.
  int    nEvent    = pythia.mode("Main:numberOfEvents");
  int    nAbort    = pythia.mode("Main:timesAllowErrors");
 
  // Initialization.
  pythia.init();

  // Begin event loop.
  int iAbort = 0; 
  for (int iEvent = 0; iEvent < nEvent; ++iEvent) {

    // Generate event. 
    if (!pythia.next()) {

      // If failure because reached end of file then exit event loop.
      if (pythia.info.atEndOfFile()) {
        cout << " Aborted since reached end of Les Houches Event File\n"; 
        break; 
      }

      // First few failures write off as "acceptable" errors, then quit.
      if (++iAbort < nAbort) continue;
      cout << " Event generation aborted prematurely, owing to error!\n"; 
      break;
    }

    if (argc > 2)
      {
	// Construct new empty HepMC event and fill it.
	// Units will be as chosen for HepMC build, but can be changed
	// by arguments, e.g. GenEvt( HepMC::Units::GEV, HepMC::Units::MM)  
	HepMC::GenEvent* hepmcevt = new HepMC::GenEvent();
	ToHepMC.fill_next_event( pythia, hepmcevt );
	
	// Write the HepMC event to file. Done with it.
	ascii_io << hepmcevt;
	delete hepmcevt;
      }

  // End of event loop. Statistics. 
  }
  pythia.stat();

  // Done.
  return 0;
}
