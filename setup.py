from setuptools import setup, find_packages

classifiers = ['Development Status :: 2 - Pre-Alpha',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: Python Software Foundation License',
               'License :: OSI Approved :: GNU General Public License (GPL)',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name = 'earthsat',
      version = '0.0.1',
      author = 'Josué M. Sehnem',
      author_email = 'josue@sehnem.com',
      description = 'Python code to download Goes16 data from aws s3 bucket',
      license = 'GPL',
      classifiers = classifiers,
      url = 'https://github.com/sehnem/earthsat',
      download_url = 'https://github.com/sehnem/earthsat/archive/0.0.1.tar.gz',
      dependency_links = [],
      install_requires = ['pandas', 'botocore', 'boto3'],
      packages = find_packages(),
      include_package_data=True,
      zip_safe=False)
