import pkg_resources
import pandas as pd


SAMPLE_DATASETS = {
    'best_prices' : ['best_prices.csv', 'best_prices'],
    'smiles_list' : ['smiles_list.csv', 'smiles_list'],
    'test_data' : ['test_data.csv', 'test_data'],
    'molport_prices_test' : ['molport_prices_test.csv', 'molport_prices_test'],
    'chemspace_prices_test' : ['chemspace_prices_test.csv', 'chemspace_prices_test'],
    'merged_prices_test' : ['merged_prices_test.csv', 'merged_prices_test'],
}

def load_data(name):
    """
    Returns one of the sample datasets.
    
    :param name: Name of the sample dataset
    :type name: string
    :returns: The Dataframe of the sample dataset
    :rtype: Dataframe
    """

    name = _select_dataset(name)

    stream = pkg_resources.resource_stream(__name__, f'data/{name}.csv')
    return pd.read_csv(stream)



def _select_dataset(name):
    """
    Returns one of the sample datasets.
    
    :param name: A version of the name of the sample dataset
    :type name: string
    :returns: The name of the sample dataset file
    :rtype: string
    """

    for key, values in SAMPLE_DATASETS.items():
        if name in values:
            return key

    raise Exception(f'"{name}" cannot be found in the sample datasets')