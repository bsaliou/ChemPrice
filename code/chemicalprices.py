import requests
import utils as utils


class PriceCollector:
    """
    A class used to plot the ECFP fingerprints of the molecules used to 
    instantiate it.
    
    :param __sim_type: similarity type structural or tailored
    :param __target_type: target type R (regression) or C (classificatino)
    :param __target: list containing the target values. Is empty if a target does not exist
    :param __mols: list of valid molecules that can be plotted
    :param __df_descriptors: datatframe containing the descriptors representation of each molecule
    :param __df_2_components: dataframe containing the two-dimenstional representation of each molecule
    :param __plot_title: title of the plot reflecting the dimensionality reduction algorithm used
    :param __data: list of the scaled descriptors to which the dimensionality reduction algorithm is applied
    :param pca_fit: PCA object created when the corresponding algorithm is applied to the data
    :param tsne_fit: t-SNE object created when the corresponding algorithm is applied to the data
    :param umap_fit: UMAP object created when the corresponding algorithm is applied to the data
    :param df_plot_xy: dataframe containing the coordinates that have been plotted
    :type __sim_type: string
    :type __target_type: string
    :type __target: list
    :type __mols: rdkit.Chem.rdchem.Mol
    :type __df_descriptors: Dataframe
    :type __df_2_components: Dataframe
    :type __plot_title: string
    :type __data: list
    :type pca_fit: sklearn.decomposition.TSNE
    :type tsne_fit: sklearn.manifold.TSNE
    :type umap_fit: umap.umap_.UMAP
    :type df_plot_xy: Dataframe
    """
    
    instances = []
    
    def __init__(self):
        self.login = {
            'molport_username': None,
            'molport_password': None,
            'molport_api_key': None,
            'chemspace_api_key': None,
            'mcule_api_key': None,
        }
        self.add_to_the_dictionnary(self)

        self.molport_id_valid = False
        self.molport_api_key_valid = False
        self.chemspace_api_key_valid = False
        self.mcule_api_key_valid = False

#------------------------------------------------------


    def add_to_the_dictionnary(self, instance):
        PriceCollector.instances.append(instance)


#------------------------------------------------------


    def setMolportUsername(self, username):
        self.login['molport_username'] = username


#------------------------------------------------------


    def setMolportPassword(self, password):
        self.login['molport_password'] = password


#------------------------------------------------------


    def setMolportApiKey(self, api_key):
        self.login['molport_api_key'] = api_key


#------------------------------------------------------


    def setChemSpaceApiKey(self, api_key):
        self.login['chemspace_api_key'] = api_key


#------------------------------------------------------


    def setMCuleApiKey(self, api_key):
        self.login['mcule_api_key'] = api_key


#------------------------------------------------------

    def status(self):
        # Display the set status of various API keys
        if (self.login['molport_username'] and self.login['molport_password']) and self.login['molport_api_key']:
            print("Status: Molport : both creditentials are set.")
        elif (self.login['molport_username'] and self.login['molport_password']) or self.login['molport_api_key']:
            print("Status: Molport : creditential is set.")
        else:
            print("Status: Molport : no credential is set.")

        if self.login['chemspace_api_key']:
            print("Status: Chemspace : creditential is set.")
        else:
            print("Status: Chemspace : no credential is set.")
            
        if self.login['mcule_api_key']:
            print("Status: MCule : creditential is set.")
        else:
            print("Status: MCule : no credential is set.")
        print("")


#------------------------------------------------------


    def check(self, Molport=True, ChemSpace=True, MCule=True):
        smiles = "CC(=O)NC1=CC=C(C=C1)O"
        value_return = 1
        a = 0
        
        if Molport:
            if self.login['molport_username'] and self.login['molport_password']:
                payload = {
                    "User Name": self.login['molport_username'],
                    "Authentication Code": self.login['molport_password'],
                    "Structure": smiles,
                    "Search Type": 5,  # Perfect research
                    "Maximum Search Time": 60000,
                    "Maximum Result Count": 1000,
                    "Chemical Similarity Index": 0.9
                }
                # Send the request to the Molport server
                r = requests.post('https://api.molport.com/api/chemical-search/search', json=payload)
                # Get the Python dictionary from the server response
                response = r.json()
                if response["Result"]["Status"] == 1:
                    self.molport_id_valid = True
                    print("Check: Molport username and password are correct.")
                    a = 1
                else:
                    print("Check: Molport username and/or password are incorrect.")
                    value_return = 0


            if self.login['molport_api_key']:
                payload = {
                    "API Key": self.login['molport_api_key'],
                    "Structure": smiles,
                    "Search Type": 5,  # Perfect research
                    "Maximum Search Time": 60000,
                    "Maximum Result Count": 1000,
                    "Chemical Similarity Index": 0.9
                }
                # Send the request to the Molport server
                r = requests.post('https://api.molport.com/api/chemical-search/search', json=payload)
                # Get the Python dictionary from the server response
                response = r.json()
                if response["Result"]["Status"] == 1:
                    self.molport_api_key_valid = True
                    print("Check: Molport api key is correct.")
                    a = 1
                else:
                    print("Check: Molport api key is incorrect.")
                    value_return = 0


        if ChemSpace:
            if self.login['chemspace_api_key']:    
                # Requires api_key
                url = "https://api.chem-space.com/auth/token"
                headers = {
                    "Authorization": f"Bearer {self.login['chemspace_api_key']}"
                }
                response = requests.get(url, headers=headers)
                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    self.chemspace_api_key_valid = True
                    print("Check: Chemspace api key is correct.")
                    a = 1
                else:
                    print("Check: Chemspace api key is incorrect.")
                    value_return = 0


        if MCule:
            if self.login['mcule_api_key']:   
                headers = {
                    'Authorization': 'Token ' + self.login['mcule_api_key'],
                }
                data = {
                    'queries': [smiles]
                }
                # Send a POST request to MCule API for exact search
                response = requests.post('https://mcule.com/api/v1/search/exact/', headers=headers, json=data)
                if response.status_code == 200:
                    self.mcule_api_key_valid = True
                    print("Check: MCule api key is correct.")
                    a = 1
                else:
                    print("Check: MCule api key is incorrect.")
                    value_return = 0
        print("")
        
        if a:
            return value_return
        return 1


#------------------------------------------------------


    def collect(self, smiles_list, progress_output=None):
        # Determine if Chemspace and/or Molport APIs are valid
        Chemspace = self.chemspace_api_key_valid
        Molport = self.molport_api_key_valid or self.molport_id_valid
        MCule = self.mcule_api_key_valid
        # Call collect_vendors function with the determined API statuses
        df = utils.collect_vendors(self, smiles_list, progress_output, Chemspace, Molport, MCule)
        
        return df


#------------------------------------------------------


    def selectBest(self, dataframe):
        if dataframe.empty:
            return dataframe
        
        # Add standardized columns to the dataframe
        dataframe = utils.add_standardized_columns(dataframe)

        # Filter the dataframe by minimum price
        df = utils.filter_csv_by_min_price(dataframe)

        return df
