import setuptools
from beefiest_rules import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="beefiest_rules",
    version=__version__,
    author="Brais Muñiz",
    author_email="mc.brais@gmail.com",
    description=
    "Tool for explaining any Machine Learning model from its predictions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bramucas/beefest_rules",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        'artificial intelligence',
        "explainable artificial intelligence"
        'logic programming',
        'answer set programming',
    ],
    python_requires='>=3.6.0',
    install_requires=[
        'clingo>=5.5.0.post3',
        'numpy',
    ],
    packages=[
        'beefiest_rules',
        'beefiest_rules.explainer',
        'beefiest_rules.parser',
        'beefiest_rules.utils',
    ],
    entry_points={
        #'console_scripts': ['xclingo=xclingo.__main__:main']
    })
