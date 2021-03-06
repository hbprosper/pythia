# pythia
Simple tools based on Pythia event generator

## Setup
Edit setup.sh if needed. In particular, the environment variable **PYTHIA8** should point 
to the location of the **lib** and **include** directories for your local installation of pythia8209. 
For example, if the shared library libpythia8.so is in $HOME/external/lib and the header
Pythia8/Pythia.h is in $HOME/external/include, then do

```
	export PYTHIA8=$HOME/external
```
Then, after cloning this repository using
```
	git clone https://github.com/hbprosper/pythia.git
```
do
```
	cd pythia
	source setup.sh
	cd bin
	make
	cd ..
```
The setup may fail because the Pythia8 script **pythia8-config** is not
	executable.  Go to the location of the script (e.g.,
	$HOME/external/bin) and make it executable using
```
	chmod +x pythia8-config
```


## Test
To test the program pythiaRun, do
```
	cd work
	pythiaRun H2ttbar.txt | tee output.log
	getxsection.py output.log | tee xsection.txt
```
The leading order cross section for p+p -> H0 + X will be written to xsection.txt.
