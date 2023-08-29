Installation
============

Installing an official release
------------------------------

There two different options you can follow to install ChemPlot.
    
Use pip
^^^^^^^^^^^^^^^^^

An alternative method is to install is using pip::

    ~$ pip install chemprices

Verify Installation
-------------------

You can verify that ChemPrices was installed on your local computer by running:

.. code-block:: bash

    ~$ pip show chemprices
    Name: chemprices
    ...

If instead of what is shown above your output is:

.. code-block:: bash

    WARNING: Package(s) not found: chemprices

ChemPrices was not installed correctly or your system cannot find the path to it. 
If ChemPrices is installed correctly you can also test the package by running:

.. code-block:: bash

    ~$ pip install pytest
    ~$ python -m pytest --pyargs chemprices

These will run all the library tests against your installation. For every official 
release from `1.2.0` you can use this command to verify that every function of
your local installation of ChemPlot works as expected.  

.. _`installation instructions for multiple platforms`: http://www.rdkit.org/docs/Install.html

    