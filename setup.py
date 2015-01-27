from setuptools import setup, find_packages

setup(
    name='harbour-pyletoh',
    version='0.1.4',
    author='Asko Soukka',
    author_email='asko.soukka@iki.fi',
    license='GPL',
    packages=find_packages('qml', exclude=['ez_setup']),
    package_dir={'': 'qml'},
    install_requires=[
        'setuptools',
    ],
    entry_points={
        'console_scripts': [
            'main.py=letoh:__main__'
        ]
    }
)
