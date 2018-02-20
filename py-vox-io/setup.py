import io, os.path, re
from setuptools import setup, find_packages


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def find_version(*file_paths):

    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='py-vox-io',
      version=find_version('pyvox', '__init__.py'),
      description='A Python parser/write for the MagicaVoxel .vox format',
      author='Gunnar Aastrand Grimnes',
      author_email='gromgull@gmail.com',
      url='https://github.com/gromgull/py-vox-io/',
      packages=find_packages(),
      license='BSD',
     )
