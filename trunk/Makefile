VERSION=$(shell ./tll --version | cut -d' ' -f2)
DISTDIR=tll-$(VERSION)
DISTFILE=$(DISTDIR).tar.bz2

all: dist

dist: deldist
	mkdir $(DISTDIR)
	cp `svn ls -rHEAD` $(DISTDIR)
	tar -cjf $(DISTFILE) $(DISTDIR)

README.html: README.txt
	rst2html $< $@

deldist:
	(test -d $(DISTDIR) && rm -fr $(DISTDIR)) || true

clean: deldist
	(test -f README.html && rm README.html) || true
	(test -f $(DISTFILE) && rm $(DISTFILE)) || true

push:
	scp $(DISTFILE) tebeka@shell.berlios.de:/home/groups/ftp/pub/tll

fresh: clean all

.PHONY: all dist clean fresh deldist push
