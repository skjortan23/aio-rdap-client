import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aio-rdap-client",
    version="0.1.8",
    author="Thomas Olofsson (@skjortan)",
    author_email="skjortan@gmail.com",
    description="An async rdap client for domain registrar information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skjortan23/aio-rdap-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # install_requires=[
    #     'aiohttp==3.6.2'
    #     'tldextract==2.2.2'
    #     'async_lru==1.0.2'
    # ],
    python_requires='>=3.7',
)
