import unittest
import pandas as pd
import os
import sys

# Add path
sys.path.insert(0, os.path.abspath('../chemicalprices'))
from chemicalprices import utils
from chemicalprices import chemicalprices as cp

# Création d'instances
instance = cp.PriceCollector()
instance.login['molport_api_key'] = "880d8343-8ui2-418c-9g7a-68b4e2e78c8b"




class TestMolportCollectPrices(unittest.TestCase):
    
    
    
    def test_empty_smiles_list(self):
        """
        Test with no smiles
        """
        # Input data
        molecule_ids = pd.DataFrame({'ID': [], 'Input SMILES': []})
        
        # function application
        df = utils.molport_collect_prices(instance, molecule_ids)  

        # Assert that the parsed data is an empty list
        self.assertTrue(df.empty)
        



class TestMolportGetIds(unittest.TestCase):
    
    
    
    def test_empty_smiles_list(self):
        """
        Test with a SMILES list is empty
        """
        # Input data
        smiles_list = []
        
        # expected result
        data = {'ID': [], 'Input SMILES': []}
        expected_result = pd.DataFrame(data, dtype=object)
        
        # Function application
        result = utils.molport_get_ids(instance, smiles_list)
        result = result.set_index(expected_result.index)
        
        # check the result
        pd.testing.assert_frame_equal(result, expected_result)
        
        
        
    
    def test_imaginary_smiles(self):
        """
        Test with imaginary SMILES is recognized
        """
        # input data
        smiles_list = ["SMILOU"]
        
        # Expected result 
        data = {'ID': [], 'Input SMILES': []}
        expected_result = pd.DataFrame(data, dtype=object)
        
        # Function application
        result = utils.molport_get_ids(instance, smiles_list)
        result = result.set_index(expected_result.index)
        
        # Check the result
        pd.testing.assert_frame_equal(result, expected_result)
        
        
        
        
    def test_single_smiles(self):
        """
        Test with a single SMILES
        """
        # Input data
        smiles_list = ["O=C(C)Oc1ccccc1C(=O)O"] # aspirin
        
        # Expected result
        new_data = {'ID': [871622], 'Input SMILES': ["O=C(C)Oc1ccccc1C(=O)O"]}
        expected_result = pd.DataFrame(new_data)
        
        # Function application
        result = utils.molport_get_ids(instance, smiles_list)
        
        # Check the result
        pd.testing.assert_frame_equal(result, expected_result)

        
        
         
    def test_multiple_smiles(self):
        """
        Test with multiple SMILES
        """
        # Input data
        smiles_list = ["CC(=O)NC1=CC=C(C=C1)O", "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", "O=C(C)Oc1ccccc1C(=O)O"]
        
        # Expected result
        data = {'ID': [150777, 47940800, 1791802, 871622], 'Input SMILES': ["CC(=O)NC1=CC=C(C=C1)O","CC(=O)NC1=CC=C(C=C1)O", "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", "O=C(C)Oc1ccccc1C(=O)O"]}
        expected_result = pd.DataFrame(data)
        
        # Function application
        result = utils.molport_get_ids(instance, smiles_list)
        
        # Check the result
        pd.testing.assert_frame_equal(result, expected_result)
        
        


class TestProcessPurity(unittest.TestCase):




    def test_process_purity(self):
        """
        Test the good formating of the purity
        """
        # Input string
        value = "('>90%',)"
        
        # Expected result
        expected_result = ">90"
        
        # Function Application
        result = utils.process_purity(value)
        
        # check the result
        self.assertEqual(result, expected_result)




    def test_process_purity_with_empty_string(self):
        """
        Test with no value 
        """
        # Input string
        value = "('',)"
        
        # Expected result
        expected_result = ""
        
        # Function application
        result = utils.process_purity(value)
        
        # Check the result
        self.assertEqual(result, expected_result)




class TestMolportStandardizeColumns(unittest.TestCase):




    def test_molport_standardize_columns_with_sample_data(self):
        """
        Test the format of standardize response
        """
        # Input data
        data = {
            'Purity': ["('',)", "('>90%',)", "('<50%',)"],
            'Currency': ['USD', 'USD', 'USD'],
            'Price': [100, 50, 75]
        }
        df = pd.DataFrame(data)
        
        # Expected DataFrame after standardization
        expected_data = {
            'Purity': ["", ">90", "<50"],
            'Price_USD': ["100", "50", "75"],
        }
        expected_df = pd.DataFrame(expected_data)

        # Call the function with the sample DataFrame
        result_df = utils.molport_standardize_columns(df)
        result_df = result_df.loc[:, ['Purity', 'Price_USD']]

        # Compare the result with the expected DataFrame
        pd.testing.assert_frame_equal(result_df, expected_df)
        
        


class TestCollectVendors(unittest.TestCase):
    
    
    
    
    def test_empty_smiles_list(self):
        """
        Test with no smiles
        """
        smiles_list = [] 
        
        data_result = utils.collect_vendors(instance, smiles_list, Molport=True, ChemSpace=False, MCule=False)  

        # Assert that the parsed data is an empty list
        self.assertTrue(data_result.empty)
        
        
        
        
    def test_wrong_smiles_list(self):
        """
        Test with a wrong smiles
        """
        smiles_list = ["wrong"] 
        
        data_result = utils.collect_vendors(instance, smiles_list, Molport=True, ChemSpace=False, MCule=False)  

        # Assert that the parsed data is an empty list
        self.assertTrue(data_result.empty)
        

        
    
if __name__ == '__main__':
    unittest.main()
