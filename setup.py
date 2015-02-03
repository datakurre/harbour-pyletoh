from setuptools import setup, find_packages

setup(
    name='harbour-pyletoh',
    version='0.3.0',
    author='Asko Soukka',
    author_email='asko.soukka@iki.fi',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'setup.py=letoh:__main__',
            'daemon.py=letoh.daemon:daemon',
            'eavesdropper.py=letoh.daemon:eavesdropper',
        ]
    }
)
