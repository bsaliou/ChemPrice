<p align="center">
  <img width="600" src="https://i.imgur.com/UHf6OV0.png">
</p>
<br />

# ChemPrice

ChemPrice is a software tool designed for the purpose of gathering pricing information for specific molecules. It is capable of retrieving price data from three different integration sources: Molport, ChemSpace, and MCule. To access these integrators, users must provide an API key for each one.

## Resources

### User Manual

You can find the detailed features and examples in the following link: [User Manual](https://).

### Web Application

ChemPrice is also available as a web application. You can use it at the following link: [Web Application](https://).

## Installation

### Use pip

ChemPrice can be installed using pip by
running:

    pip install chemprice

## How to use Chemprice

### Getting started

ChemPrice requires a list of molecule SMILES as the representation of molecules:

```python
smiles_list = ["CC(=O)NC1=CC=C(C=C1)O", "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", "O=C(C)Oc1ccccc1C(=O)O"]
```

First, we need to create an instance from the PriceCollector class. Using this instance, we'll be able to connect to the various integrators and then launch a search
on the list of smiles entered.

```python
from chemiprice import PriceCollector
pc = PriceCollector()
```

### Request an API key

To access integrators' data, you need to be able to connect to their API.

If you don't have an API key yet, you can click on the following links :
[Molport](https://www.molport.com/shop/user-api-keys),
[ChemSpace](https://chem-space.com/contacts) and
[MCule](https://mcule.com/contact/),
which will take you back to their sites where you can request an API key.

### Set the API key for each integrator

Now, an instance from the `PriceCollector` class has been created, we need to connect to one
or more integrators via an API key.

Connection to Molport via API key:

```python
pc.setMolportApiKey("880d8343-8ui2-418c-9g7a-68b4e2e78c8b")
```

In the case of Molport, it's also possible to log in with a login and password.

```python
pc.setMolportUsername("john.spade")
pc.setMolportPassword("fasdga34a3")
```

To check the status of each key, run the following method :

```python
pc.status()
```

Possible Outputs

```python
# Username/Password and API Key are Set:
Status: Molport: both credentials are set.

# Only Username/Password or API Key is Set:
Status: Molport: credential is set.

# No Credential is Set:
Status: Molport: no credential is set.
```

Similar to the Molport connection, for ChemSpace and MCule, the approach is the same. However, ChemSpace and MCule require only an API key. You need to use
the :mod:`setChemSpaceApiKey()` and :mod:`setMCuleApiKey()` functions, such as :

```python
pc.setChemSpaceApiKey(<chemspace_api_key>)
pc.setMCuleApiKey(<mcule_api_key>)
```

### Price Search

Before starting the price search, check the validity of the API keys entered.

```python
pc.check()
```

Possible Outputs:

```python
# API Key is Set and correct:
Check: Molport API key is correct.

# API Key is Set but not correct:
Check: Molport API key is incorrect.
```

If the identifiers checked are correct, then it's possible
to run the method :mod:`collect()` to obtain all the information
found on the molecule. The price is given in USD according to
the units and quantity entered by the vendor. The units of measurement
for quantities are categorized into three families: mols, grams, and liters.

```python
all_prices = pc.collect()
```

The output will be a dataframe containing all price information about the molecule.

| Input Smiles          | Source  | Supplier Name         | Purity | Amount | Measure | Price_USD |
| --------------------- | ------- | --------------------- | ------ | ------ | ------- | --------- |
| CC(=O)NC1=CC=C(C=C1)O | Molport | "ChemDiv, Inc."       | >90    | 100    | mg      | 407.1     |
| CC(=O)NC1=CC=C(C=C1)O | Molport | MedChemExpress Europe | 98.83  | 10     | g       | 112.8     |
| CC(=O)NC1=CC=C(C=C1)O | Molport | TargetMol Chemicals   | 100.0  | 500    | mg      | 50.0      |

With the :mod:`selectBest()` function, you can keep only the best prices for each molecule.
In fact, for each unit of measurement (mol gram and liter) the results are compared
to find the best quantity/price ratio.

```python
pc.selectBest(all_prices)
```

The output will be a dataframe containing only the best quantity/price ratio of each molecule.

| Input Smiles          | Source  | Supplier Name       | Purity | Amount | Measure  | Price_USD | USD/g  | USD/mol            |
| --------------------- | ------- | ------------------- | ------ | ------ | -------- | --------- | ------ | ------------------ |
| CC(=O)NC1=CC=C(C=C1)O | Molport | Cayman Europe       | >=98   | 500    | g        | 407.1     | 0.22   |                    |
| O=C(C)Oc1ccccc1C(=O)O | Molport | Cayman Europe       | >=90   | 500    | g        | 112.8     | 0.1606 |                    |
| O=C(C)Oc1ccccc1C(=O)O | Molport | Life Chemicals Inc. | >90    | 20     | micromol | 50.0      |        | 3950000.0000000005 |

### Contact

For any question you can contact us through email:

- [Baptiste Saliou](mailto:baptiste1saliou@gmail.com)
