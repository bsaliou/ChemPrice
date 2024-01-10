Installation
============

Installing an official release
------------------------------

There two different options you can follow to install ChemPlot.
    
Use pip
^^^^^^^^^^^^^^^^^

An alternative method is to install is using pip::

    ~$ pip install chemprice

Verify Installation
-------------------

You can verify that ChemPrice was installed on your local computer by running:

.. code-block:: bash

    ~$ pip show chemprice
    Name: chemprice
    ...

If instead of what is shown above your output is:

.. code-block:: bash

    WARNING: Package(s) not found: chemprice

ChemPrice was not installed correctly or your system cannot find the path to it. 
If ChemPrice is installed correctly you can also test the package by running:

.. code-block:: bash

    ~$ pip install pytest
    ~$ pytest chemprice/tests/


    