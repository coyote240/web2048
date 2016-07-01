from setuptools import setup

setup(
    name='web2048',
    version='0.1',
    description='Demo py2048 online.',
    author='Adam A.G. Shamblin',
    author_email='adam.shamblin@tutanota.com',
    license='MIT',
    install_requires=[
        'tornado>=4',
        'honcho>=0.6'
    ])
