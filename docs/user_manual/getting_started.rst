How to use Chemical Price Research
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

Possible Outputs:

1. Username/password and api key are set:
   - "Status: Molport: both credentials are set."

2. Only the username/password or the api key is set:
   - "Status: Molport: credential is set."

3. No credential is set:
   - "Status: Molport: no credential is set."

Check the validity of identifiers
--------------------

To now visualize the chemical space of the dataset we use :mod:`visualize_plot()`.

.. code:: python3

    import matplotlib.pyplot as plt

    cp.visualize_plot()
    
.. image:: images/gs_tsne.png
   :width: 600

The second figure shows the results obtained by reducing the dimensions of features Principal Component Analysis (PCA) [3]_.

.. code:: python3

    cp.pca()
    cp.visualize_plot()

.. image:: images/gs_pca.png
   :width: 600

The third figure shows the results obtained by reducing the dimensions of features by UMAP [4]_.

.. code:: python3

    cp.umap()
    cp.visualize_plot()

.. image:: images/gs_umap.png
   :width: 600

In each figure the molecules are coloured by class value. 


.. _`RDKit chemistry framework`: http://www.rdkit.org

--------------

.. raw:: html

   <h3>

References:

.. raw:: html

    </h3>
    
.. [1] **Martins, Ines Filipa, et al.** (2012). `A Bayesian approach to in silico blood-brain barrier penetration modeling. <https://pubmed.ncbi.nlm.nih.gov/22612593/>`__ Journal of chemical information and modeling 52.6, 1686-1697
.. [2] **van der Maaten, Laurens, Hinton, Geoffrey.** (2008). `Viualizingdata using t-SNE. <https://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf?fbclid=IwAR0Bgg1eA5TFmqOZeCQXsIoL6PKrVXUFaskUKtg6yBhVXAFFvZA6yQiYx-M>`__ Journal of Machine Learning Research. 9. 2579-2605.
.. [3] **Wold, S., Esbensen, K., Geladi, P.** (1987). `Principal component analysis. <https://www.sciencedirect.com/science/article/abs/pii/0169743987800849>`__ Chemometrics and intelligent laboratory systems. 2(1-3). 37-52.
.. [4] **McInnes, L., Healy, J., Melville, J.** (2018). `Umap: Uniform manifold approximation and projection for dimension reduction. <https://arxiv.org/abs/1802.03426>`__ arXivpreprint arXiv:1802.03426.