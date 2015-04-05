import glob
from os.path import abspath, basename, dirname, join as pjoin


SAMPLE_DIR = abspath(pjoin(dirname(__file__), 'sample_gpg_files'))


SAMPLE_FILES = [(basename(fn), fn)
                for fn in glob.glob(pjoin(SAMPLE_DIR, '*.gpg'))]
