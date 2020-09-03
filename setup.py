import setuptools

setuptools.setup(
    name="vprint",
    version="0.0.1",
    author="Vidar Magnusson",
    author_email="vprint@vidarmagnusson.com",
    description="A printing utiliy for chalmers university printers",
    long_description="",
    url="https://github.com/viddem/vprint",
    packages=["src"],
    entry_points="""
    [console_scripts]
    vprint = src.cli:print_file_to_printer
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)