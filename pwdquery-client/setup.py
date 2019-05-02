import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pwdquery-client",
    version="0.0.1",
    author="Max Harley",
    author_email="maxh@maxh.io",
    description="pwdquery client executable",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pwdquery-socket'],
    url="http://maxh.io",
    packages=['pwdquery.client'],
    classifiers=[],
    entry_points={
        'console_scripts': ['pwdquery=pwdquery.client.__main__:main']
    })
