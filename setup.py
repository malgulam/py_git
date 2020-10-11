import setuptools
import pygit
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="py_git",
    version=0.1,
    author="druzgeorge",
    description="Essentially: Pythonically Git.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/malgulam/PyGit",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
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
