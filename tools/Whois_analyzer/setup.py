#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='whois-analyzer',
    version='0.1.0',
    description='Công cụ tra cứu và phân tích thông tin WHOIS cho tên miền',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='I3Cwg',
    author_email='pi3cuong@gmail.com',
    url='https://github.com/example/whois-analyzer',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: System :: Systems Administration',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'whois-analyzer=whois_analyzer.cli:main',
        ],
    },
)