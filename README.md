# Documentation for mailcomposer.
# mailcomposer is a light wrapper to [premailer](https://pypi.org/project/premailer/) for use in Django projects.

It inlines css styles in html documents to make them usable in emails.
It can inline css in single html files or all the html files in a directory.

Because this app is tailored for use in django, some of the options from premailer have been set
to their defaults and can't be changed, however, we will add support to the rest of premailer options if their is 
public request for it.

# INSTALLATION
+ Install mailify using pip or clone the github repo.
+ Add ***'mailcomposer'*** to INSTALLED_APPS list in the Django settings file
	- This app is dependent on the Django settings `BASE_DIR`

# USAGE
	python manage.py mailcomposer --indir --outdir --infile --outfile --stylepath --network

`--indir` is the directory containing the html files to be inlined relative to your project root,
if this directory has sub folders,
html files therein will also have their CSS inlined.

+ **NOTE**: indir goes with outdir, which specifies the path also relative to your project root where 
output html will be stored, however, if no output dir is specified, the files in the indir will be overwritten with the html files.

`--outdir` is the directory where the output files will be stored.

`--infile` in case you just want to transform a single file, it should go with '--outfile' else '--infile is overwritten'

`--outfile` the output file to write the transformed file to, it works with only '--infile'.

`--stylepath` the path to directory containing stylesheets which you want to inline.

`--network` this is a flag which toggles network access to be access stylesheets over the nework
