'''
Date: 2021-02-28 17:06:01
LastEditors: Rustle Karl
LastEditTime: 2021.06.24 17:16:23
'''
import os.path

from setuptools import setup

__version__ = '1.0.4'

# What packages are required for this module to be executed?
requires = [
    'project-pkgs',
]

# Import the README and use it as the long-description.
cwd = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ffmpeg-generator',
    packages=[
        'ffmpeg',
        'ffmpeg.expression',
        'ffmpeg.filters',
        'ffmpeg.tools',
        'ffmpeg.transitions',
    ],
    version=__version__,
    license='MIT',
    author='Rustle Karl',
    author_email='fu.jiawei@outlook.com',
    description='Python bindings for FFmpeg - with almost all filters support, even `gltransition` filter.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fujiawei-dev/ffmpeg-generator',
    keywords=['ffmpeg', 'ffprobe', 'ffplay'],
    classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
    ],
    install_requires=requires,
)
