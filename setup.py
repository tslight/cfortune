import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cfortune",
    version="0.0.1",
    author="Toby Slight",
    author_email="tobyslight@gmail.com",
    description="Curses Fortune Browser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tslight/cfortune",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'cfortune = cfortune.__main__:main',
        ],
    }
)
