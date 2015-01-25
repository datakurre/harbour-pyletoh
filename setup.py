from setuptools import setup, find_packages

setup(
    name='harbour-myletoh',
    version='1.0.0',
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
            'main.py=app:__main__'
        ]
    }
)
