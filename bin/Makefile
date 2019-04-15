ifndef PYTHIA8
$(error PYTHIA8 not defined! export PYTHIA8=location of lib directory for libpythia8.so)
endif
# name of Pythia
NAME:=pythiaRun
CXX:=g++

bin: $(NAME)

$(NAME): 
	$(CXX) $(CXXFLAGS) -Wno-shadow -I$(PYTHIA8)/include \
	$@.cc -o $@ \
	-L$(PYTHIA8)/lib -lpythia8 -lLHAPDF -lHepMC -ldl

clean:
	rm -rf $(NAME) $(NAME).o
