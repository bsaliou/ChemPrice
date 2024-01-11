How to use ChemPrice
===================

ChemPrice is a software designed to simplify the gathering of pricing data from more than 100 suppliers by integrating with ChemSpace, Mcule, and Molport platforms. It ensures uniformity in pricing units, providing comprehensive and optimized pricing details for specified compounds.

Getting started
---------------
First, let's create a list of molecules in SMILES notation to be searched:
  
.. code:: python3

    smiles_list = ["CC(=O)NC1=CC=C(C=C1)O", "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", "O=C(C)Oc1ccccc1C(=O)O"]

Next, create an instance from the PriceCollector class. Using this instance,  we'll be able to connect to the various integrators and then launch a search 
on the list of SMILES entered.

.. code:: python3

    from chemprice import PriceCollector
    
    pc = PriceCollector()

Requesting an API key
--------------------

To access integrators' data, we need to be able to connect to their API. 

If you don't have an API key yet, you can request one via the following links : 
`Molport <https://www.molport.com/shop/user-api-keys>`_, 
`ChemSpace <https://chem-space.com/contacts>`_ and 
`MCule <https://mcule.com/contact/>`_.

Enter the API key for each integrator
--------------------

Now that the ``PriceCollector`` class has been created, we need to connect to one 
or more integrators via an API key. 

Connection to Molport via API key: 880d8343-8ui2-418c-9g7a-68b4e2e78c8b

.. code:: python3
    
    pc.setMolportApiKey("880d8343-8ui2-418c-9g7a-68b4e2e78c8b")

In the case of Molport, it's also possible to log in with a login and password. 
ChemSpace and Mcule support only API keys.

.. code:: python3
    
    pc.setMolportUsername("john.spade")
    pc.setMolportPassword("fasdga34a3")

To check the status of each key, run the : 

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

Price Search
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

If the credentials checked are correct, then it's possible 
to run the method :mod:`collect()` to obtain the price information 
found on the molecule. The prices are given in USD according to 
the units and quantity entered by the vendor. The units of measurement 
for quantities are categorized into three families: moles, grams, and liters.

.. code:: python3

    all_prices = pc.collect(smiles_list)

The output will be a dataframe containing all price information of the molecules in the search list.

+-----------------------+---------+-----------------------+--------+--------+---------+-----------+
| Input Smiles          | Source  | Supplier Name         | Purity | Amount | Measure | Price_USD |
+=======================+=========+=======================+========+========+=========+===========+
| CC(=O)NC1=CC=C(C=C1)O | Molport | "ChemDiv, Inc."       | >90    | 100    | mg      | 407.1     |
+-----------------------+---------+-----------------------+--------+--------+---------+-----------+
| CC(=O)NC1=CC=C(C=C1)O | Molport | MedChemExpress Europe | 98.83  | 10     | g       | 112.8     |
+-----------------------+---------+-----------------------+--------+--------+---------+-----------+
| CC(=O)NC1=CC=C(C=C1)O | Molport | TargetMol Chemicals   | 100.0  | 500    | mg      | 50.0      |
+-----------------------+---------+-----------------------+--------+--------+---------+-----------+

With the :mod:`selectBest()` function, we can select the best prices for each molecule. 
In fact, for each unit of measurement (mol, gram, and liter) the results are calculated separately 
to find the best quantity/price ratio. 

.. code:: python3

    pc.selectBest(all_prices)

The output will be a dataframe containing only the best quantity/price ratio for each molecule.

+-----------------------+---------+---------------------+--------+--------+----------+-----------+--------+--------------------+
| Input Smiles          | Source  | Supplier Name       | Purity | Amount | Measure  | Price_USD | USD/g  | USD/mol            |
+=======================+=========+=====================+========+========+==========+===========+========+====================+
| CC(=O)NC1=CC=C(C=C1)O | Molport | Cayman Europe       | >=98   | 500    | g        | 407.1     | 0.22   |                    |
+-----------------------+---------+---------------------+--------+--------+----------+-----------+--------+--------------------+
| O=C(C)Oc1ccccc1C(=O)O | Molport | Cayman Europe       | >=90   | 500    | g        | 112.8     | 0.1606 |                    |
+-----------------------+---------+---------------------+--------+--------+----------+-----------+--------+--------------------+
| O=C(C)Oc1ccccc1C(=O)O | Molport | Life Chemicals Inc. | >90    | 20     | micromol | 50.0      |        | 3950000.0000000005 |
+-----------------------+---------+---------------------+--------+--------+----------+-----------+--------+--------------------+
