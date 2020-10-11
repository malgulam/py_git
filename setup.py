import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="PyGit",
    version="0.1",
    author="druzgeorge",
    description="Essentially: Pythonically Git.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/malgulam/PyGit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI  Approved :: MIT License",
        "Operating System :: OS Independent",
        "Windows OS Support :: In Progress",
        "Intended Audience ::  Developers",
        "Topic :: Software Development :: Version Control Systems :: Git",
        "Topic :: Autonomization Of Git Processes"
    ],
    keywords='Essentially: Pythonically Git.',
    download_url='https://github.com/malgulam/PyGit/archive/master.zip',
    license='MIT',
    install_requires=[
        'requirements.txt'
    ],
    zip_safe= False,
    python_requires='>=3.6',
)