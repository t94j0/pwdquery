import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pwdquery-server",
    version="0.0.1",
    author="Max Harley",
    author_email="maxh@maxh.io",
    description="pwdquery server library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pwdquery-socket'],
    url="http://maxh.io",
    packages=['pwdquery.server', 'pwdquery.server.store'],
    classifiers=[],
    entry_points={
        'console_scripts': ['pwdqueryd=pwdquery.server.__main__:main']
    })
