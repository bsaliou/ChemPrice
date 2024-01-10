Development Environment 
=======================

The development environment is an installation of ChemPrice on your local computer
which can be used for testing existing features or developing new ones in order 
to contribute to the library.

Then clone your forked GitHub repository of `ChemPrice <https://github.com/bsaliou/ChemPrice>`_ on your local computer using 
either HTTPS:

.. code-block:: bash

    ~$ git clone https://github.com/<your-username>/ChemPrice.git

Or using SSH:

.. code-block:: bash

    ~$ git clone git@github.com:<your-username>/ChemPrice.git

Then from the terminal navigate to the ChemPrice repository you just created. 
You can now install ChemPrices in editable mode. Editable mode will allow your code
changes to be propagated through the library code without having to reinstall. 

.. code-block:: bash

    ~/<PATH-TO-CLONE>/ChemPrice$ pip install -e .

You are now ready to develop ChemPrice!

Testing 
-------

To run the unit tests for ChemPrice use this command:

.. code-block:: bash

    ~$ pytest chemprice/tests/