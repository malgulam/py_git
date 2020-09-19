import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = "PyGit-druzgeorge",
    vesion="0.0.1",
    author="George M.B-Y.J",
    author_email = "geobillyand@gmail.com",
    description="A Python VC tool",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/malgulam/PyGit#pygit",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)