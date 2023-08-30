import pandas as pd
import requests
import time
import re
from tqdm import tqdm


######################################################################
"------------------------------Molport-------------------------------"
######################################################################


# Collects molport ids from the given list smiles (we will use this ids to search)
def molport_get_ids(instance, smiles_list):
    # List to store t he IDs and SMILES
    id_smiles_list = []

    molport_username = instance.login['molport_username']
    molport_password = instance.login['molport_password']
    molport_api_key = instance.login['molport_api_key']
        
    for smiles in tqdm(smiles_list):
        # Data to send to the Molport server
        if molport_username != None:
            payload = {
                "User Name": molport_username,
                "Authentication Code": molport_password,
                "Structure": smiles,
                "Search Type": 5, # Perfect research
                "Maximum Search Time": 60000,
                "Maximum Result Count": 1000,
                "Chemical Similarity Index": 0.9
            }

        else:
            payload = {
                "API Key": molport_api_key,
                "Structure": smiles,
                "Search Type": 5, # Perfect research
                "Maximum Search Time": 60000,
                "Maximum Result Count": 1000,
                "Chemical Similarity Index": 0.9
            }

        # Send the request to the Molport server
        r = requests.post('https://api.molport.com/api/chemical-search/search', json=payload)

        # Get the Python dictionary from the server response
        response = r.json()

        if response["Result"]["Status"] == 1:
            molecules = response["Data"]["Molecules"]

            # Iterate over the molecules and their information
            for molecule in molecules:
                molecule_id = molecule["Id"]
                id_smiles_list.append((molecule_id, smiles))

    df = pd.DataFrame(id_smiles_list, columns=["ID", "Input SMILES"])

    return df


######################################################################
######################################################################


#cleans the purity text
def process_purity(value):
    if value == "('',)":
        return ""
    else:
        return value.strip('\'(%\'),')

# standardize the price and purity columns with chemspace data   
def molport_standardize_columns(data):
    
    data = data.astype(str)
    
    # Apply the custom function to the 'Purity' column
    data['Purity'] = data['Purity'].apply(process_purity)

    # Create new columns Price_USD and Price_EUR with empty strings
    data['Price_USD'] = ""

    # Replace relevant values with corresponding prices
    data.loc[data['Currency'] == 'USD', 'Price_USD'] = data.loc[data['Currency'] == 'USD', 'Price']

    # Remove the Price and Currency columns
    data.drop(['Price', 'Currency'], axis=1, inplace=True)
    
    return data


######################################################################
######################################################################


# Collects prices for the given ids and coverts them into dataframe
def molport_collect_prices(instance, molecule_ids):
    """
    Collects price data for molecules from Molport API.

    :param instance: The PriceCollector instance containing API credentials.
    :param molecule_ids: DataFrame containing molecule IDs and SMILES.
    :type instance: PriceCollector
    :type molecule_ids: pandas.DataFrame
    :return: DataFrame containing collected price data.
    :rtype: pandas.DataFrame
    """
    all_molecules_data = []

    molport_username = instance.login['molport_username']
    molport_password = instance.login['molport_password']
    molport_api_key = instance.login['molport_api_key']

    for _, row in tqdm(molecule_ids.iterrows(),total=len(molecule_ids)):
        molecule_id = row['ID']
        smiles = row['Input SMILES']

        if molport_username != None:
            # Molport API URL using the API key and molecule ID
            url = f'https://api.molport.com/api/molecule/load?molecule={molecule_id}&username={molport_username}&authenticationcode={molport_password}'
        else:
            url = f'https://api.molport.com/api/molecule/load?molecule={molecule_id}&apikey={molport_api_key}'

        # Send the POST request to the Molport API
        response = requests.post(url)

        # Check the response status
        if response.status_code == 200:
            # The request was successful
            data = response.json()
            data['Data']['Molecule']['Input SMILES'] = smiles
            all_molecules_data.append(data)
        else:
            # The request failed
            print(f'Error in the request for molecule {molecule_id}: {response.status_code}')


    molport_data = []
    
    for data_ in all_molecules_data:
            input_smiles = data_['Data']['Molecule']['Input SMILES']
            smiles = data_['Data']['Molecule']['SMILES']
            supplier_data = data_["Data"]["Molecule"]["Catalogues"]["Screening Block Suppliers"]

            # Write each data row
            for supplier in supplier_data:
                supplier_name = supplier["Supplier Name"]
                catalogues = supplier["Catalogues"]

                for catalogue in catalogues:
                    purity = catalogue.get("Purity", ""),

                    last_update_date = catalogue.get("Last Update Date Exact", "")
                    packings = catalogue["Available Packings"]

                    for packing in packings:
                        
                        source = "Molport"
                        amount = packing.get("Amount", "")
                        measure = packing.get("Measure", "")
                        price = packing.get("Price", "")
                        currency = packing.get("Currency", "")
                        
                    molport_data.append((source, input_smiles, smiles, last_update_date, supplier_name, purity, price, amount, measure, currency))

    # Create a DataFrame with collected data
    df = pd.DataFrame(molport_data, columns=["Source", "Input SMILES", "SMILES", "Last Update Date Exact", "Supplier Name", "Purity", "Price", "Amount", "Measure", "Currency"])

    # read the file again
    df = molport_standardize_columns(df)

    #remove if no price rows
    df = df.dropna(subset=["Price_USD"], how='all')
    return df


######################################################################
"----------------------------ChemSpace-------------------------------"
######################################################################


# requires api_key
def chemspace_get_token(instance):

    chemspace_api_key = instance.login['chemspace_api_key']

    url = "https://api.chem-space.com/auth/token"
    headers = {
        "Authorization": f"Bearer {chemspace_api_key}"
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Retrieve the access token from the response
        access_token = response.json()["access_token"]

        return access_token
    else:
        # The request failed, print the status code and response content
        print("The request failed with the status code:", response.status_code)
        return None
    

######################################################################
######################################################################


# Collects prices for the given SMILES and coverts them into dataframe
def chemspace_collect_prices(instance, smiles_list):
    """
    Collects price data for molecules from ChemSpace API.

    :param instance: The PriceCollector instance containing API credentials.
    :param smiles_list: list containing molecule SMILES.
    :type instance: PriceCollector
    :type smiles_list: list
    :return: DataFrame containing collected price data.
    :rtype: pandas.DataFrame
    """

    access_token = chemspace_get_token(instance)
    url = "https://api.chem-space.com/v3/search/exact"
    headers = {
        "Accept": "application/json; version=3.1",
        "Authorization": "Bearer " + access_token,
    }
    params = {
        "count": 3,
        "page": 1,
        "categories": "CSCS,CSMB"
    }

    response_data = []

    for index, smiles in tqdm(enumerate(smiles_list),total=len(smiles_list)):
        data = {
            "SMILES": smiles
        }

        response = requests.post(url, headers=headers, data=data, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Process the response here
            molecule_data = response.json()

            # original smiles added
            for item in molecule_data['items']:
                item['input smiles'] = smiles

            response_data.append(molecule_data)
        else:
            # The request failed, print the status code and response content
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)

        # Pause for 1.5 seconds between each request
        if index < len(smiles_list) - 1:
            time.sleep(1.5)

    chemspace_data = []
    
    # Iterate through the elements of the JSON file
    for data in response_data:
        for item in data['items']:
            for offer in item['offers']:
                for price in offer['prices']:
                    
                    source = "ChemSpace"
                    input_smiles = item['input smiles']
                    smiles = item["smiles"]
                    cas = item["cas"]
                    supplier_name = offer['vendorName']
                    purity = offer['purity']
                    amount = price['pack']
                    measure = price['uom']
                    price_usd = price['priceUsd']

                    chemspace_data.append((source, input_smiles, smiles, cas, supplier_name, purity, amount, measure, price_usd))
                    
    df = pd.DataFrame(chemspace_data, columns=["Source", "Input SMILES", "SMILES", "CAS", "Supplier Name", "Purity", "Amount", "Measure", "Price_USD"])
    df = df.dropna(subset=["Price_USD"], how='all')

    return df


######################################################################
"-------------------------------MCule--------------------------------"
######################################################################


# Function to collect MCule IDs with respect to limits
def mcule_get_ids(mcule_token, smiles_list):
    id_smiles_list = []

    headers = {
        'Authorization': 'Token ' + mcule_token,
    }

    # Iterate through smiles_list while respecting the limits
    for i in range(0, len(smiles_list), 500):  # Process 500 SMILES at a time
        batch_smiles = smiles_list[i:i+500]  # Extract a batch of SMILES

        data = {
            'queries': batch_smiles
        }

        # Send a POST request to MCule API for exact search
        response = requests.post('https://mcule.com/api/v1/search/exact/', headers=headers, json=data)

        if response.status_code == 200:
            results = response.json()["results"]

            # Extract MCule IDs and corresponding SMILES
            for result in results:
                molecule_id = result["mcule_id"]
                query = result["query"]
                id_smiles_list.append((molecule_id, query))

    # Create a DataFrame with collected data
    df = pd.DataFrame(id_smiles_list, columns=["ID", "Input SMILES"])
    return df



# Function to build packages for multiple amounts
def build_packages(mcule_token, df):
    if df.empty:
        return
    # Define the API URL
    url = "https://mcule.com/api/v1/iquote-queries/"

    # Headers for authorization
    headers = {
        "Authorization": "Token " + mcule_token,
        "Content-Type": "application/json",
        "Accept": "application/json, */*",
        "Accept-Encoding": "gzip, deflate"
    }

    package_ids = []  # List to store package IDs

    amount_list = ["1", "5", "10", "100", "1000", "10000", "100000", "1000000"]

    for index,amount in tqdm(enumerate(amount_list),total=len(amount_list)):
        # Request body in JSON format
        data = {
            "amount": amount,
            "customer_first_name": "John",
            "customer_last_name": "Doe",
            "delivery_country": "US",
            "mcule_ids": df["ID"].tolist(),
            "min_amount": None
        }

        # Send the POST request
        response = requests.post(url, json=data, headers=headers)

        # Check the response
        if response.status_code == 201:  # Status code 201 for Created
            results = response.json()
            package_id = results["id"]
            package_ids.append(package_id)  # Add package ID to the list
        else:
            print("POST request failed for amount:", amount)
            print("Response code:", response.status_code)
            print(response.text)

    return package_ids


######################################################################
######################################################################


# Function to get quotes
def get_quotes(token, quote):
    for quote_data in quote.get('group', {}).get('quotes', []):
        quote_id = quote_data['id']
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json',
        }
        url = f'https://mcule.com/api/v1/iquotes/{quote_id}/'
        response = requests.get(url, headers=headers)
        yield response.json()


# Function to collect prices and data from MCule API
def mcule_collect_prices(instance, package_ids):
    """
    Collects price data for molecules from MCule API.

    :param instance: The PriceCollector instance containing API credentials.
    :param package_ids: list containing molecule package IDs.
    :type instance: PriceCollector
    :type package_ids: list
    :return: DataFrame containing collected price data.
    :rtype: pandas.DataFrame
    """
    
    token = instance.login['mcule_api_key']
    
    data = []
    
    if package_ids is None:
        # Create a DataFrame with collected data
        df = pd.DataFrame(data, columns=["Source", "ID", "Supplier Name", "SMILES", "Purity", "Price_USD", "Amount", "Measure"])
        return df

    # Define headers for authorization
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
    }

    for index, package_id in tqdm(enumerate(package_ids),total=len(package_ids)):

        # Construct the URL for the specific quote request
        url = f'https://mcule.com/api/v1/iquote-queries/{package_id}/'

        # Function to check the status of the quote request
        def check_status():
            response_package = requests.get(url, headers=headers).json()
            status = response_package['state']
            if status == 40:
                return None
            elif status == 30 and response_package['group']:
                return response_package
            elif status == 30 and not response_package['group']:
                return None
            else:
                return 1

        response_package = check_status()
        while response_package == 1:
            time.sleep(0.5)
            response_package = check_status()

        if response_package is None:
            continue

        for quote in get_quotes(token, response_package):
            # Extract values from each product item in the quote
            product_items = quote.get('items', [])

            for item in product_items:
                source = "MCule"
                mcule_id = item.get('structure_origin_mcule_id')
                product_supplier_name = item.get('product_supplier_name')
                smiles = item.get('product_smiles')
                purity = item.get('product_purity')
                price = item.get('product_price')
                amount = item.get('amount')
                measure = "mg"
                data.append((source, mcule_id, product_supplier_name, smiles, purity, price, amount, measure))

    # Create a DataFrame with collected data
    df = pd.DataFrame(data, columns=["Source", "ID", "Supplier Name", "SMILES", "Purity", "Price_USD", "Amount", "Measure"])

    return df

# Merges two dataframes
def add_input_smiles_columns(df1, df2):

    # Common columns to use for merging
    common_columns = ['ID']

    # Convert columns to compatible data types
    df1 = df1.astype(str)
    df2 = df2.astype(str)

    # Merge the two dataframes using the common columns
    merged_df = pd.merge(df1, df2, on=common_columns, how='outer')

    # Sort dataframe
    merged_df = merged_df.sort_values(by=['Input SMILES'])
    merged_df.drop("ID", axis=1, inplace=True)
    merged_df = merged_df.dropna(subset=['SMILES'])
    merged_df = merged_df.drop_duplicates()

    return merged_df


######################################################################
"--------------------------Data operation----------------------------"
######################################################################


def merge_dataframes(df_list):
    # Common columns to use for merging
    common_columns = ['Source', 'Input SMILES', 'SMILES', 'Supplier Name', 'Purity', 'Amount', 'Measure', 'Price_USD']

    # Initialize an empty dataframe to store the merged results
    merged_df = pd.DataFrame(columns=common_columns)

    # Convert columns to compatible data types for all dataframes in the list
    for i in range(len(df_list)):
        df_list[i] = df_list[i].astype(str)

    # Merge all dataframes in the list using the common columns
    for df in df_list:
        merged_df = pd.merge(merged_df, df, on=common_columns, how='outer')

    # Sort dataframe
    merged_df = merged_df.sort_values(by=['Input SMILES'])

    # Save the merged dataframe to a new CSV file
    # merged_df.to_csv("merged_prices.csv", index=False)

    return merged_df


######################################################################
######################################################################


# Define conversion factors for different measures
conversion_factors = {
    # Conversion to g
    'kg': 1000,
    'g': 1,
    'mg': 1 / 1000,
    'microg': 1 / 1000000,
    'ug': 1 / 1000000,

    # Conversion to mol
    'kmol': 1000,
    'mol': 1,
    'mmol': 1 / 1000,
    'micromol': 1 / 1000000,
    'umol': 1 / 1000000,

    # Conversion to l
    'kl': 1000,
    'l': 1,
    'ml': 1 / 1000,
    'mL': 1 / 1000,
    'microl': 1 / 1000000,
    'ul': 1 / 1000000,
}


######################################################################
######################################################################


# parses the units like 5x100g
def extract_unit_bulk(unit_string):
    # Extract the numeric part and unit from the unit string
    parts = re.search(r'(\d+)x(\d+)(\D+)', unit_string)
    if parts:
        bulk = int(parts.group(1)) * int(parts.group(2))
        unit = parts.group(3).lower()
        return bulk, unit
    else:
        bulk = re.search(r'\d+', unit_string)
        if bulk:
            bulk = int(bulk.group())
        else:
            return None, None

        unit = re.search(r'[a-zA-Z]+', unit_string)
        if unit:
            unit = unit.group().lower()
        else:
            return None, None

#Convert all prices into USD/g or USD/mol or USD/l
def standardize_prices(row):
    measure = row['Measure']
    amount = float(row['Amount'])
    price = float(row['Price_USD'])

    if measure in conversion_factors:
        return price / (conversion_factors[measure] * amount)
    else:
        bulk, unit = extract_unit_bulk(measure)
        if amount and unit:
            if unit in conversion_factors:
                return price / (conversion_factors[unit] * (amount * bulk))
        print("Unknown measure units for:",measure)
        return None
    
def add_standardized_columns(df):

    if df.empty:
        # Empty dataframe, add empty columns and save
        df['USD/g'] = ''
        df['USD/mol'] = ''
        df['USD/l'] = ''
        return df

    df['Measure'] = df['Measure'].astype(str)

    # Apply the function to create new columns
    df['USD/g'] = df.apply(lambda row: standardize_prices(row) if row['Measure'] in ['g', 'mg', 'kg', 'microg', 'ug' ] or re.match(r'\d+x\d+g', row['Measure']) else None, axis=1)
    df['USD/mol'] = df.apply(lambda row: standardize_prices(row) if row['Measure'] in ['mol', 'micromol', 'mmol', 'kmol', 'umol'] else None, axis=1)
    df['USD/l'] = df.apply(lambda row: standardize_prices(row) if (row['Measure'] in ['ml', 'microl', 'l', 'mL', 'kl', 'ul']) or re.match(r'\d+x\d+mL', row['Measure']) else None, axis=1)

    # Sort and Save the dataframe with the additional columns to a new CSV file
    df = df.sort_values(by=['Input SMILES', 'USD/g', 'USD/mol', 'USD/l'])
    # df.to_csv("standardized_merged_prices.csv", index=False)
    return df


######################################################################
######################################################################


def filter_csv_by_min_price(df):

    # Remove rows where neither of the two values (USD/g and USD/mol) is present
    df = df.dropna(subset=["USD/g", "USD/mol", "USD/l"], how='all')

    # Filter the rows from the initial dataframe, keeping only those corresponding to the smallest value of "Price_USD"
    filtered_df_g = df[df.groupby("Input SMILES")["USD/g"].transform(min) == df["USD/g"]]
    filtered_df_mol = df[df.groupby("Input SMILES")["USD/mol"].transform(min) == df["USD/mol"]]
    filtered_df_l = df[df.groupby("Input SMILES")["USD/l"].transform(min) == df["USD/l"]]

    # If multiple rows have the same price, keep the first one
    filtered_df_g = filtered_df_g.sample(frac=1).groupby("Input SMILES", as_index=False).first()
    filtered_df_mol = filtered_df_mol.sample(frac=1).groupby("Input SMILES", as_index=False).first()
    filtered_df_l = filtered_df_l.sample(frac=1).groupby("Input SMILES", as_index=False).first()

    # Combine the results using concatenation
    filtered_df = pd.concat([filtered_df_g, filtered_df_mol, filtered_df_l])

    filtered_df = filtered_df.sort_values(by=['Input SMILES', 'USD/g', 'USD/mol', 'USD/l'])
    
    return filtered_df


######################################################################
######################################################################


def collect_vendors(instance, smiles_list, progress_output=None, ChemSpace=True, Molport=True, MCule=True):
    
    time_start  = time.perf_counter()
    
    nb_integrator = sum([ChemSpace, Molport, MCule])
    progress = 0
    
    # List of selected suppliers
    selected_providers = []

    if Molport:
        # Get the molecule IDs and print count MolPort
        print(f"Collecting ID's for given {len(smiles_list)} SMILES from MolPort...")
        df_molecule_ids = molport_get_ids(instance, smiles_list)
        smiles_exists = df_molecule_ids['Input SMILES'].nunique()
        print(f"Total: {smiles_exists} molecules and {len(df_molecule_ids)} conformers are found in MolPort.\n")
        progress += 3/(4*nb_integrator)
        if progress_output is not None:
            progress_output.append(progress) 

        # Get the prices and print count from MolPort
        print(f"Collecting Prices for given {len(smiles_list)} IDs from MolPort...")
        molport_prices=molport_collect_prices(instance, df_molecule_ids)
        smiles_with_price = molport_prices.loc[molport_prices['Price_USD'].notnull(), 'Input SMILES'].nunique()
        print(f"Total: {len(molport_prices)} prices for {smiles_with_price} molecules are found in MolPort.\n")
        progress += 1/(4*nb_integrator)
        if progress_output is not None:
            progress_output.append(progress) 
        selected_providers.append(("Molport", molport_prices))

    if ChemSpace:
        # Get the prices and print count from ChemSpace
        print(f"Collecting Prices for given {len(smiles_list)} SMILES from ChemSpace...")
        chemspace_prices=chemspace_collect_prices(instance, smiles_list)
        unique_smiles_count = chemspace_prices['Input SMILES'].nunique()
        smiles_with_price_cs = len(chemspace_prices[chemspace_prices['Price_USD'].notnull()])
        print(f"Total: {smiles_with_price_cs} prices for {unique_smiles_count} molecules are found in ChemSpace.\n")
        progress += 1/nb_integrator
        if progress_output is not None:
            progress_output.append(progress) 
        selected_providers.append(("ChemSpace", chemspace_prices))
        
    if MCule:
        # Get the molecule IDs and print count MolPort
        mcule_token = instance.login['mcule_api_key']
        print(f"Collecting ID's for given {len(smiles_list)} SMILES from MCule...")
        df_molecule_ids = mcule_get_ids(mcule_token, smiles_list)
        smiles_exists = df_molecule_ids['Input SMILES'].nunique()
        package_id = build_packages(mcule_token, df_molecule_ids)
        print(f"Total: {smiles_exists} molecules and {len(df_molecule_ids)} conformers are found in MCule.\n")
        progress += 1/(2*nb_integrator)
        if progress_output is not None:
            progress_output.append(progress) 

        # Get the prices and print count from MCule
        print(f"Collecting Prices for given {len(smiles_list)} IDs from MCule...")
        mcule_prices = mcule_collect_prices(mcule_token, package_id)
        mcule_prices = add_input_smiles_columns(df_molecule_ids, mcule_prices)
        smiles_with_price = mcule_prices.loc[mcule_prices['Price_USD'].notnull(), 'Input SMILES'].nunique()
        print(f"Total: {len(mcule_prices)} prices for {smiles_with_price} molecules are found in MCule.\n")
        progress += 1/(2*nb_integrator)
        if progress_output is not None:
            progress_output.append(progress)  
        selected_providers.append(("MCule", mcule_prices))

    if selected_providers:
        name_providers = [row[0] for row in selected_providers]
        if len(name_providers) >= 2:
            all_providers = ", ".join(name_providers[:-1]) + " and " + name_providers[-1]
        else:
            all_providers = name_providers[0]
        print(f"Merging Results from {all_providers}...")
        merged_df = merge_dataframes([row[1] for row in selected_providers])
        unique_smiles_count_merged = merged_df['Input SMILES'].nunique()
        smiles_with_price_merged = len(merged_df.loc[merged_df['Price_USD'].notnull(), 'Input SMILES'])
        print(f"Total: {smiles_with_price_merged} prices for {unique_smiles_count_merged} molecules exist in the Merged file.\n")
    else:
        print(f"The credentials are missing or incorrect. You need to set credential for at least one integrator.")
        return pd.DataFrame([])

    time_end = time.perf_counter()
    print(f"Total time: {time_end - time_start:0.4f} seconds")
    print(f"Vendor price collection is successfully done!")
    
    if progress_output is not None:
        progress_output.append(1.0)  # Ensure completion
    
    return merged_df
