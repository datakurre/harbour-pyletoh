from setuptools import setup, find_packages

setup(
    name='harbour-pyletoh',
    version='0.6.4',
    author='Asko Soukka',
    author_email='asko.soukka@iki.fi',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    install_requires=[
        'PyTweening'
    ],
    entry_points={
        'console_scripts': [
            'setup.py=letoh:__main__',
            'service.py=letoh.daemons:letoh_service',
            'eavesdropper.py=letoh.daemons:letoh_eavesdropper',
        ]
    }
)
