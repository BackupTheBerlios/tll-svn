# Makefile for "Little Lanuncher" project
# You'll need:
# Python (http://www.python.org)
# py2exe ()

# Miki Tebeka <miki.tebeka@zoran.com>
# $Id$

ifeq ($(OSTYPE),cygwin)
	PYTHON = ${shell cygpath -au `cmd /c pyexe.py`}
else # win32
	PWD = ${shell cmd /c cd}
	PATH := $(PWD)\bin;$(PATH)
	PYTHON = $(shell cmd /c pyexe.py)
endif

DIST = launch
WDIST = launch_w32.zip
UDIST = launch.zip
SDIST = launch_src.zip
README = README.txt
RC = launchrc

SOURCES = Makefile README.txt _launchrc .launchrc bin launch.pyw pyexe.py \
		  setup.py sr2lu

all: 
	@echo
	@echo please choose "alldist", "dist", "w32dist" or "srcdist"
	@echo

alldist: dist srcdist w32dist

w32dist: $(WDIST)

pre:
	rm -fr $(DIST)
	mkdir $(DIST)
	cp $(README) $(DIST)

$(WDIST): pre launch.pyw setup.py $(README) _$(RC)
	$(PYTHON) setup.py py2exe -d $(DIST)
	cp _$(RC) $(DIST)
	zip -r9 $(WDIST) $(DIST)

dist: $(UDIST)

$(UDIST): pre launch.pyw $(README) .$(RC)
	cp launch.pyw $(DIST)/launch
	cp .$(RC) $(DIST)
	zip -r9 $(UDIST) $(DIST)

srcdist: $(SDIST)

$(SDIST): pre $(SOURCES)
	cp -r $(SOURCES) $(DIST)
	rm -fr $(DIST)/bin/.svn
	zip -r9 $(SDIST) $(DIST)

clean:
	rm -f *.pyc
	rm -fr build $(DIST)
	rm -f $(WDIST) $(UDIST) $(SDIST)

.PHONY: all clean pre w32dist srcdist dist alldist
