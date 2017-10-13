from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_description = file.read()

with open('ipfromwebpage/requirements.txt', 'r') as file:
    requirements = file.readlines()

with open('tests/requirements-test.txt', 'r') as file:
    requirements_test = file.readlines()

setup(
    name='ip-from-webpage',
    version='1.0',
    url='https://github.com/shepherdjay/ip-from-webpage',
    license='MIT',
    author='Jay Shepherd',
    author_email='jdshep89@hotmail.com',
    description='Takes a webpage and outputs all ip address scope.',
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['tests*']),
    install_requires=requirements,
    tests_requires=requirements_test,
)
