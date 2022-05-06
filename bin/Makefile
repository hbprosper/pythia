# name of Pythia
NAME	:= pythiaRun
CXX	:= clang++

PYTHIA8FLAGS	:= $(shell pythia8-config --cxxflags)
PYTHIA8LIBS	:= $(shell pythia8-config --libs)

HEPMC3FLAGS	:= $(shell HepMC3-config --cxxflags)
HEPMC3LIBS	:= $(shell HepMC3-config --libs)

bin: 	$(NAME)

$(NAME): 
	$(CXX) $(CXXFLAGS) -Wno-shadow $(HEPMC3FLAGS) $(PYTHIA8FLAGS) \
	$@.cc -o $@ \
	$(PYTHIA8LIBS) $(HEPMC3LIBS) -lLHAPDF -ldl

clean:
	rm -rf $(NAME) $(NAME).o
