import setuptools

setuptools.setup(
    name="printit-vidde",
    version="1.2.2",
    author="Vidar Magnusson",
    author_email="printit@vidarmagnusson.com",
    description="A printing utiliy for chalmers university printers",
    long_description="",
    url="https://github.com/viddem/printit",
    packages=["src"],
    entry_points="""
    [console_scripts]
    printit = src.cli:cli
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: AGPL3 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)