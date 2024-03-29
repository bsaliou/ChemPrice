from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chemprice", 
    version="1.1.0",
    author="Baptiste SALIOU",
    author_email="baptiste1saliou@gmail.com",
    description="A python library for chemical price Search.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bsaliou/ChemPrice",
    project_urls={
        "Interface": "https://chemprice.streamlit.app/",
	    "Documentation": "https://chemprice.readthedocs.io/en/latest/"
    },
    license="BSD",
    packages=["chemprice", "chemprice.tests", "."],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering"
    ],
    keywords="chemoinformatics",
    install_requires=[    
        "requests==2.28.1",
        "pandas==1.3.5",
        "tqdm==4.65.0"
    ],
    test_suite="pytest",
    tests_require=[
        "pytest>=7.0.0",
    ],
    include_package_data=True,
    package_data={'tests': ['data/*.csv'], '': ['logo/*.png']},
    python_requires='>=3.6',
)