CLINVAR=ClinVarFullRelease_2017-05.xml

all: clinvar.c.norm clinvar.g.norm
	bin/process.py clinvar.c.norm c clinvar.sqlite
	bin/process.py clinvar.g.norm g clinvar.sqlite

clinvar.c.norm: clinvar.c.res
	bin/preprocess.py clinvar.c.res c clinvar.sqlite clinvar.c.norm

clinvar.g.norm: clinvar.g.res
	bin/preprocess.py clinvar.g.res g clinvar.sqlite clinvar.g.norm

clinvar.c.res: clinvar.c
	bin/normalize.py clinvar.c > clinvar.c.res

clinvar.g.res: clinvar.g
	bin/normalize.py clinvar.g > clinvar.g.res

clinvar.c: clinvar.sqlite
	echo "select var_c from clinvar where var_c is not NULL;" | sqlite3 clinvar.sqlite > clinvar.c

clinvar.g: clinvar.sqlite
	echo "select var_g from clinvar where var_g is not NULL;" | sqlite3 clinvar.sqlite > clinvar.g

clinvar.sqlite: $(CLINVAR)
	cat sql/clinvar.sql | sqlite3 clinvar.sqlite
	bin/xml2sqlite.py $(CLINVAR) clinvar.sqlite 2>origin_duplicates.tsv

$(CLINVAR):
	wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/$(CLINVAR).gz
	gzip -d $(CLINVAR).gz

clean:
	rm -f clinvar.c clinvar.g clinvar.c.res clinvar.g.res clinvar.c.norm clinvar.g.norm
