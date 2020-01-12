"""
usage mailify --indir --outdir --infile --outfile --stylepath --network.

1. if you have your styles stored in the django static directory and linked to in your html file
you can give the absolute path to the file containing the stylesheet.
2. if you referenced styles in other web locations e.g CDNs you can enable network mode with --network flag
3. if you have relative urls in your html file, you can can add a url with --baseUrl <https://example.com/>
"""
from django.core.management.base import BaseCommand, CommandError
from premailer import transform
import os
from django.conf import settings
from collections import deque

class Command(BaseCommand):
	help = 'inline the css styles in html documents'

	def add_arguments(self, parser):
		parser.add_argument('--indir',
			help='the folder containing the html files relative to the project\'s base',
			type=str)
		parser.add_argument('--outdir',
			help="""the folder the transformed html files should be stored relative to the project's base.
					If this is not provided, the original files are overwritten, this folder is created if it does not exist""",
			type=str)
		parser.add_argument('--infile',
			help="""the html file to be transformed, relative to the base of the project.
			if indir is defined, this argument is thrown out """, 
			type=str)
		parser.add_argument('--outfile',
			help="""the html file to which the transformed html will be written,
			if this is not provided, the original html document is overwritten""",
			type=str)
		parser.add_argument('--stylepath',
			help="The absolute path to the the stylesheet",
			type=str)

		parser.add_argument('--network',
			help="Toggle network mode on",
			default=True,
			action='store_true')

	def handle(self, *args, **options):
		self._indir = self._outdir = self._outfile = self._infile = self._indir = self._basepath = None
		if options['indir']:
			self._indir = os.path.join(
				settings.BASE_DIR,
				self._remove_slash(options['indir']))
		if options['outdir']:
			self._outdir = os.path.join(
				settings.BASE_DIR,
				self._remove_slash(options['outdir']))
		if options['infile']:
			self._infile = os.path.join(
				settings.BASE_DIR, 
				self._remove_slash(options['infile']))
		if options['outfile']:
			self._outfile = os.path.join(
				settings.BASE_DIR, 
				self._remove_slash(options['outfile']))
		if options['stylepath']:
			self._basepath = os.path.join(
				settings.BASE_DIR,
				self._remove_slash(options['stylepath']))
		self._network = options['network']
		if not settings.BASE_DIR:
			raise CommandError('Your django settings file does not define a BASE_DIR value.')
		if self._indir:
			return self._source_from_dir()
		if self._infile:
			return self._source_from_file()
		raise CommandError('You did not specify any source file or folder')

	def _source_from_file(self):
		if not os.path.exists(self._infile):
			raise CommandError('The input file does not exist')
		if not self._outfile:
			self.stdout.write(
				self.style.WARNING(
					"""No output file was specified, the input file will be overwritten with the output,
					type ctrl+c to cancel if you don\'t want that to happen"""))
		if self._outdir and not os.path.exists(os.path.dirname(self._outdir)):
			raise CommandError('The directory for the output does not exist, please create it and try again')
		self._transform(self._infile, self._outfile)
		self.stdout.write(self.style.SUCCESS('Styles in {} have been inlined'.format(self._infile)))


	def _source_from_dir(self):
		if not os.path.exists(self._indir):
			raise CommandError('The input dir does not exist')
		if not self._outdir:
			self._outdir = self._indir
			self.stdout.write(
				self.style.WARNING(
					"""No output directory was specified, the input dir will be overwritten with the output,
					type ctrl+c to cancel if you don\'t want that to happen"""))
		dir_tree = deque([self._indir])
		while True:
			"""
			Big picture of this section of code.

			the original directory provided was put in a queue above, from where it is popped and
			scanned listing the files and subdirectories in it,
			the files are transformed while the subdirectories are added to the queue, this process is repeated for all the 
			subdirectories on queue until there is none left.
			"""
			contents = os.scandir(dir_tree.popleft())
			dir_contents = [content for content in contents]  # This looks weird but I did it to make the iterator `contents` reuseable
			dirs = [dir_content.path for dir_content in dir_contents if dir_content.is_dir()]
			files = [content.path for content in dir_contents if content.is_file() and '.html' in content.name]
			dir_tree.extend(dirs)
			for file in files:
				outfile = file
				if self._indir != self._outdir:
					outfile = os.path.join(self._outdir, 
						self._remove_slash(file.replace(self._indir, '')))  # cut off the path of the input dir from the filepath
					outpath = os.path.dirname(outfile)
					if not os.path.exists(outpath):
						os.makedirs(outpath)
				self._transform(file, outfile)
			if not dir_tree:
				break
		self.stdout.write(
			self.style.SUCCESS(
				'Styles in {} have been inlined and moved to {}'.format(self._indir, self._outdir)))



	def _transform(self, infile, outfile=None):
		outfile = outfile or infile
		html = self.read_file(infile)
		output = transform(html=html, allow_network=self._network, base_path=self._basepath)
		self.write_file(outfile, output)

	def _remove_slash(self, string):
		if not string:
			return string
		first_char = string[0]
		last_char = string[-1]
		if first_char == '/' or first_char == '\\':
			string = '' + string[1:]
		if last_char == '/' or last_char == '\\':
			string = string[0:-1] + ''
		return string

	def read_file(self, filepath):
		with open(filepath, 'r+') as file:
			content = file.read()
		return content

	def write_file(self, filepath, content):
		with open(filepath, 'w+') as file:
			file.write(content)


				

