from setuptools import setup, find_packages

setup(
    name='plex-api', 
    version='0.1.0', 
    author='Chase Davies',
    author_email='plex-api-module@chasedavies.net',
    description='A Python wrapper for interacting with Plex Media Server API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chasepd/plex-api',
    packages=find_packages(),
    install_requires=[
        'requests', 
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7.9',  
)
