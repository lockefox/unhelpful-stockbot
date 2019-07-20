"""packaging tools for unhelpful-stockbot"""
from codecs import open
from setuptools import setup, find_packages

with open('README.md', 'r') as rm_fh:
    __readme__ = rm_fh.read()

with open('VERSION', 'r') as v_fh:
    __version__ = v_fh.read().strip()

__package_name__ = 'unhelpful-stockbot'


setup(
    name=__package_name__,
    author='John Purcell',
    author_email='jpurcell.ee@gmail.com',
    description='Slackbot for generating (unhelpful) stock quotes',
    long_description=__readme__,
    long_description_content_type='text/markdown',
    version=__version__,
    url='TODO',
    license='MIT',
    classifiers=['Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7'],
    keywords='slack bot stock fintech chatbot',
    packages=find_packages(),
    package_data={'': ['LICENSE', 'README.md', 'VERSION'], 'unhelpful': ['app.cfg']},
    install_requires=['slackbot==0.5.3', 'requests==2.22.0'],
    entry_points={'console_scripts': ['launch-unhelpful=unhelpful.bot:run']},
)
