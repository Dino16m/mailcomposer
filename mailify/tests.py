from io import StringIO
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.conf import settings
import os

__BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@override_settings(BASE_DIR=__BASE_DIR)
class MailifyTest(TestCase):	

	def untab(self, string):
		replacement_list = ['\n', '\t']
		for s in replacement_list:
			string = string.replace(s, '')
		return string

	def read_file(self, filepath):
		with open(filepath, 'r') as file:
			data = file.read()
		return data

	def write_file(self, filepath, content):
		with open(filepath, 'w+') as file:
			file.write(content)


	def test_infile_only(self):
		out = StringIO()
		infile = 'test_templates/mails/indir/mail1.html'
		orig_mail = self.read_file(infile)
		call_command('mailify', infile=infile, stdout=out)
		self.write_file(infile, orig_mail)
		self.assertIn(self.untab("""No output file was specified, the input file will be overwritten with the output,
						type ctrl+c to cancel if you don\'t want that to happen"""),
						self.untab(out.getvalue()))
		self.assertIn("Styles in {} have been inlined".format(os.path.join(settings.BASE_DIR, infile)), out.getvalue())

	def test_infile_outfile(self):
		out = StringIO()
		infile = 'test_templates/mails/indir/mail1.html'
		outfile = 'test_templates/mails/outdir/mail1.html'
		call_command('mailify', infile=infile, outfile=outfile, stdout=out)
		self.assertIn("Styles in {} have been inlined".format(os.path.join(settings.BASE_DIR, infile)), out.getvalue())
		self.assertTrue(
			os.path.exists(os.path.join(settings.BASE_DIR, outfile)))
		os.remove(os.path.join(settings.BASE_DIR, outfile))

	def test_indir_only_unnested(self):
		out = StringIO()
		indir = 'test_templates/mails/indir/submails'
		orig_mail1 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail1.html'))
		orig_mail2 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail2.html'))
		orig_mail3 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail3.html'))
		call_command('mailify', indir=indir, stdout=out)
		new_mail1 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail1.html'))
		new_mail2 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail2.html'))
		new_mail3 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail3.html'))
		self.write_file(os.path.join(settings.BASE_DIR, indir, 'mail1.html'), orig_mail1)
		self.write_file(os.path.join(settings.BASE_DIR, indir, 'mail2.html'), orig_mail2)
		self.write_file(os.path.join(settings.BASE_DIR, indir, 'mail3.html'), orig_mail3)
		self.assertNotEqual(orig_mail1, new_mail1)
		self.assertNotEqual(orig_mail2, new_mail2)
		self.assertNotEqual(orig_mail3, new_mail3)
		self.assertIn(self.untab(
			"""No output directory was specified, the input dir will be overwritten with the output,
					type ctrl+c to cancel if you don\'t want that to happen"""),
			self.untab(out.getvalue()))
		inpath = os.path.join(settings.BASE_DIR, indir)
		self.assertIn(
			"Styles in {} have been inlined and moved to {}".format(inpath, inpath),
			self.untab(out.getvalue()))

	def test_indir_outdir_unnested(self):
		out = StringIO()
		indir = 'test_templates/mails/indir/submails'
		outdir = 'test_templates/mails/outdir/submails'
		orig_mail1 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail1.html'))
		orig_mail2 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail2.html'))
		orig_mail3 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail3.html'))
		call_command('mailify', indir=indir, outdir=outdir, stdout=out)
		self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, outdir, 'mail1.html')))
		self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, outdir, 'mail2.html')))
		self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, outdir, 'mail3.html')))
		new_mail1 = self.read_file(os.path.join(settings.BASE_DIR, outdir, 'mail1.html'))
		new_mail2 = self.read_file(os.path.join(settings.BASE_DIR, outdir, 'mail2.html'))
		new_mail3 = self.read_file(os.path.join(settings.BASE_DIR, outdir, 'mail3.html'))
		self.assertNotEqual(orig_mail1, new_mail1)
		self.assertNotEqual(orig_mail2, new_mail2)
		self.assertNotEqual(orig_mail3, new_mail3)
		os.remove(os.path.join(settings.BASE_DIR, outdir, 'mail1.html'))
		os.remove(os.path.join(settings.BASE_DIR, outdir, 'mail2.html'))
		os.remove(os.path.join(settings.BASE_DIR, outdir, 'mail3.html'))
		inpath = os.path.join(settings.BASE_DIR, indir)
		outpath = os.path.join(settings.BASE_DIR, outdir)
		self.assertIn(
			"Styles in {} have been inlined and moved to {}".format(inpath, outpath),
			self.untab(out.getvalue()))

	def test_indir_only_nested(self):
		out = StringIO()
		indir = 'test_templates/mails/indir'
		orig_mail1 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail1.html'))
		orig_mail2 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail2.html'))
		orig_mail3 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail3.html'))
		orig_mail4 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'submails', 'mail1.html'))
		orig_mail5 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'submails', 'mail2.html'))
		orig_mail6 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'submails', 'mail3.html'))
		call_command('mailify', indir=indir, stdout=out)
		new_mail1 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail1.html'))
		new_mail2 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail2.html'))
		new_mail3 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail3.html'))
		new_mail4 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'submails', 'mail1.html'))
		new_mail5 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'submails', 'mail2.html'))
		new_mail6 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'submails', 'mail3.html'))
		self.write_file(os.path.join(settings.BASE_DIR, indir, 'mail1.html'), orig_mail1)
		self.write_file(os.path.join(settings.BASE_DIR, indir, 'mail2.html'), orig_mail2)
		self.write_file(os.path.join(settings.BASE_DIR, indir, 'mail3.html'), orig_mail3)
		self.write_file(os.path.join(settings.BASE_DIR, indir, 'submails', 'mail1.html'), orig_mail4)
		self.write_file(os.path.join(settings.BASE_DIR, indir, 'submails', 'mail2.html'), orig_mail5)
		self.write_file(os.path.join(settings.BASE_DIR, indir, 'submails', 'mail3.html'), orig_mail6)
		self.assertNotEqual(orig_mail1, new_mail1)
		self.assertNotEqual(orig_mail2, new_mail2)
		self.assertNotEqual(orig_mail3, new_mail3)
		self.assertNotEqual(orig_mail4, new_mail4)
		self.assertNotEqual(orig_mail5, new_mail5)
		self.assertNotEqual(orig_mail6, new_mail6)
		self.assertIn(self.untab(
			"""No output directory was specified, the input dir will be overwritten with the output,
					type ctrl+c to cancel if you don\'t want that to happen"""),
			self.untab(out.getvalue()))
		inpath = os.path.join(settings.BASE_DIR, indir)
		self.assertIn(
			"Styles in {} have been inlined and moved to {}".format(inpath, inpath),
			self.untab(out.getvalue()))

	def indir_outdir_nested(self):
		out = StringIO()
		indir = 'test_templates/mails/indir'
		outdir = 'test_templates/mails/outdir'
		orig_mail1 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail1.html'))
		orig_mail2 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail2.html'))
		orig_mail3 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'mail3.html'))
		orig_mail4 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'submails', 'mail1.html'))
		orig_mail5 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'submails', 'mail2.html'))
		orig_mail6 = self.read_file(os.path.join(settings.BASE_DIR, indir, 'submails', 'mail3.html'))
		call_command('mailify', indir=indir, outdir=outdir, stdout=out)
		self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, outdir, 'mail1.html')))
		self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, outdir, 'mail2.html')))
		self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, outdir, 'mail3.html')))
		self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, outdir, 'submails', 'mail1.html')))
		self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, outdir, 'submails', 'mail2.html')))
		self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, outdir, 'submails', 'mail3.html')))
		new_mail1 = self.read_file(os.path.join(settings.BASE_DIR, outdir, 'mail1.html'))
		new_mail2 = self.read_file(os.path.join(settings.BASE_DIR, outdir, 'mail2.html'))
		new_mail3 = self.read_file(os.path.join(settings.BASE_DIR, outdir, 'mail3.html'))
		new_mail4 = self.read_file(os.path.join(settings.BASE_DIR, outdir, 'submails', 'mail1.html'))
		new_mail5 = self.read_file(os.path.join(settings.BASE_DIR, outdir, 'submails', 'mail2.html'))
		new_mail6 = self.read_file(os.path.join(settings.BASE_DIR, outdir, 'submails', 'mail3.html'))
		self.assertNotEqual(orig_mail1, new_mail1)
		self.assertNotEqual(orig_mail2, new_mail2)
		self.assertNotEqual(orig_mail3, new_mail3)
		self.assertNotEqual(orig_mail4, new_mail4)
		self.assertNotEqual(orig_mail5, new_mail5)
		self.assertNotEqual(orig_mail6, new_mail6)
		os.remove(os.path.join(settings.BASE_DIR, outdir, 'mail1.html'))
		os.remove(os.path.join(settings.BASE_DIR, outdir, 'mail2.html'))
		os.remove(os.path.join(settings.BASE_DIR, outdir, 'mail3.html'))
		os.remove(os.path.join(settings.BASE_DIR, outdir, 'submails', 'mail1.html'))
		os.remove(os.path.join(settings.BASE_DIR, outdir, 'submails', 'mail2.html'))
		os.remove(os.path.join(settings.BASE_DIR, outdir, 'submails', 'mail3.html'))
		inpath = os.path.join(settings.BASE_DIR, indir)
		outpath = os.path.join(settings.BASE_DIR, outdir)
		self.assertIn(
			"Styles in {} have been inlined and moved to {}".format(inpath, outpath),
			self.untab(out.getvalue()))





