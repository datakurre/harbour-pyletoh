from setuptools import setup, find_packages

setup(
    name='harbour-pyletoh',
    version='0.2.1',
    author='Asko Soukka',
    author_email='asko.soukka@iki.fi',
    license='GPL',
    packages=find_packages('qml', exclude=['ez_setup']),
    package_dir={'': 'qml'},
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'app.py=letoh:__main__'
        ]
    }
)
