import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dbcurses",
    version="0.0.1",
    author="Lykos94",
    scripts=['dbcurses'],
    author_email="lukaszmoskwa94@gmail.com",
    description="Curses-based application for database visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lykos94/dbcurses",
    packages=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix"
    ],
    python_requires='>=3.6',
)
