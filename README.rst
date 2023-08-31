   <p align="center">
     <img width="600" src="logo/logo_chemprice_transparent.png">
   </p>
   <br />


How to use ChemPrice
===================

ChemPrices is a computer tool that allows retrieving the prices of molecules 
from their SMILES using various integrators. ChemPrices supports three 
integrators: Molport, ChemSpace, and MCule. Each integrator requires an API 
key to be used.

Getting started
---------------
To demonstrate how to use the functions, you need to create a list of molecule SMILES:
  
.. code:: python3

    smiles_list = ["CC(=O)NC1=CC=C(C=C1)O", "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", "O=C(C)Oc1ccccc1C(=O)O"]

Next, create a first instance with the PriceCollector class. It's from this class 
that we'll be able to connect to the various integrators and then launch a search 
on the list of smiles entered.

.. code:: python3

    from chemicalprices import PriceCollector
    
    pc = PriceCollector()

Request an api key
--------------------

To access integrators' data, you need to be able to connect to their api. 

If you don't have an api key yet, you can click on the following links : 
`Molport <https://www.molport.com/shop/user-api-keys>`_, 
`ChemSpace <https://chem-space.com/contacts>`_ and 
`MCule <https://mcule.com/contact/>`_,
which will take you back to their sites where you can request an api key.

Enter the API key for each integrator
--------------------

Now that the ``PriceCollector`` class has been created, we need to connect to one 
or more integrators via an api key. 

Connection to Molport via api key: 880d8343-8ui2-418c-9g7a-68b4e2e78c8b

.. code:: python3
    
    pc.setMolportApiKey("880d8343-8ui2-418c-9g7a-68b4e2e78c8b")

In the case of molport, it's also possible to log in with a login and password. 
ChemSpace and MCule require an api key.

.. code:: python3
    
    pc.setMolportUsername("john.spade")
    pc.setMolportPassword("fasdga34a3")

To check the status of each key that has been returned to the class, run the : 

.. code:: python3
    
    pc.status()

Possible Outputs

.. code:: python3

    # Username/Password and API Key are Set:
    Status: Molport: both credentials are set.

    # Only Username/Password or API Key is Set:
    Status: Molport: credential is set.

    # No Credential is Set:
    Status: Molport: no credential is set.

In these examples, we're only talking about the Molport connection; 
for ChemSpace and MCule, the approach is the same. You need to use 
the :mod:`setChemSpaceApiKey()` and :mod:`setMCuleApiKey()` functions, such as :

.. code:: python3

    pc.setChemSpaceApiKey(<chemspace_api_key>)
    pc.setMCuleApiKey(<mcule_api_key>)

Price search
--------------------

Before starting the price search, check the validity of the api keys entered. 

.. code:: python3

    pc.check()

Possible Outputs:

.. code:: python3

    # API Key is Set and correct:
    Check: Molport api key is correct.

    # API Key is Set but not correct:
    Check: Molport api key is incorrect.

If the identifiers checked are correct, then it's possible 
to run the method :mod:`collect()` to obtain all the information 
found on the molecule. The price is given in USD according to 
the units and quantity entered by the vendor. The units of measurement 
for quantities are categorized into three families: moles, grams, and liters.

.. code:: python3

    all_prices = pc.collect()

The output will be a dataframe containing all price information about the molecule.

+-----------------------+---------+-----------------------+--------+--------+---------+-----------+
| Input Smiles          | Source  | Supplier Name         | Purity | Amount | Measure | Price_USD |
+=======================+=========+=======================+========+========+=========+===========+
| CC(=O)NC1=CC=C(C=C1)O | Molport | "ChemDiv, Inc."       | >90    | 100    | mg      | 407.1     |
+-----------------------+---------+-----------------------+--------+--------+---------+-----------+
| CC(=O)NC1=CC=C(C=C1)O | Molport | MedChemExpress Europe | 98.83  | 10     | g       | 112.8     |
+-----------------------+---------+-----------------------+--------+--------+---------+-----------+
| CC(=O)NC1=CC=C(C=C1)O | Molport | TargetMol Chemicals   | 100.0  | 500    | mg      | 50.0      |
+-----------------------+---------+-----------------------+--------+--------+---------+-----------+

With the :mod:`selectBest()` function, you can keep only the best prices for each molecule. 
In fact, for each unit of measurement (mol gram and liter) the results are compared 
to find the best quantity/price ratio. 

.. code:: python3

    pc.selectBest(all_prices)

The output will be a dataframe containing only the best quantity/price ratio about each molecule.

+-----------------------+---------+---------------------+--------+--------+----------+-----------+--------+--------------------+
| Input Smiles          | Source  | Supplier Name       | Purity | Amount | Measure  | Price_USD | USD/g  | USD/mol            |
+=======================+=========+=====================+========+========+==========+===========+========+====================+
| CC(=O)NC1=CC=C(C=C1)O | Molport | Cayman Europe       | >=98   | 500    | g        | 407.1     | 0.22   |                    |
+-----------------------+---------+---------------------+--------+--------+----------+-----------+--------+--------------------+
| O=C(C)Oc1ccccc1C(=O)O | Molport | Cayman Europe       | >=90   | 500    | g        | 112.8     | 0.1606 |                    |
+-----------------------+---------+---------------------+--------+--------+----------+-----------+--------+--------------------+
| O=C(C)Oc1ccccc1C(=O)O | Molport | Life Chemicals Inc. | >90    | 20     | micromol | 50.0      |        | 3950000.0000000005 |
+-----------------------+---------+---------------------+--------+--------+----------+-----------+--------+--------------------+
