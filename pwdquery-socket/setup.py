import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pwdquery-socket",
    version="0.0.1",
    author="Max Harley",
    author_email="maxh@maxh.io",
    description="Socket connection library for socket.socket",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://maxh.io",
    packages=['pwdquery.socket'],
    classifiers=[],
)
