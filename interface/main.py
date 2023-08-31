import sys
import streamlit as st
import pandas as pd
import base64
import time
import tempfile
import os
import threading
import time
from streamlit.runtime.scriptrunner import add_script_run_ctx
from pathlib import Path

# Ajouter le deuxième chemin d'accès
sys.path.insert(0, os.path.abspath('../chemicalprices'))
import chemicalprices as cp

DEFAULT_STATUS = 1
INIT_STATUS = 2

NB_INTEGRATORS = 3

LIMIT_SMILES = 100

######################
# CREATION CLASS AND PAGE
######################

pc = cp.PriceCollector()
st.set_page_config(page_title="ChemPrice Web Application", layout="wide")

emptycont=st.empty()
home1=emptycont.container()
st.session_state.result = pd.DataFrame([])

if 'new_page'not in st.session_state:      
    st.session_state["new_page"] = False


######################
# DEFINE IMAGES
######################

# Convert a file into base 64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# Green check logo
def logo_check(chemin_image):
    # Convertir les données binaires en base64 pour l'affichage HTML
    image_base64 = get_base64(chemin_image)
    return f'<img src="data:image/jpeg;base64,{image_base64}" alt="Image" width="15">'

# ChemPrice logo
def logo_chemprice(chemin_image):
    # Convertir les données binaires en base64 pour l'affichage HTML
    image_base64 = get_base64(chemin_image)
    return f'<img src="data:image/jpeg;base64,{image_base64}" alt="Image" width="250">'


# Background of the window
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)



######################
# FUNCTIONS DEFINITION
######################

def back_fun():
    st.session_state["new_page"]=False


def but_click(check_integrator):
    if st.session_state.input_smiles == "":
        st.warning("No SMILES selected")
    elif not check_integrator:
        st.warning("No Integrator selected")
    else :
        st.session_state["new_page"]=True


# Initialize integrator status
def initialize_integrator(integrator_name):
    if f'activate_{integrator_name}' not in st.session_state:
        st.session_state[f'activate_{integrator_name}'] = DEFAULT_STATUS


# Create integrator checkbox and activation status
def create_integration_column(col, integrator_name):
    sub_col = col.columns([0.07, 0.93])
    option = sub_col[0].checkbox(" ", key=f"{integrator_name}_box")

    # Display integration status based on activation
    if st.session_state[f'activate_{integrator_name}'] == INIT_STATUS:
        path = Path(__file__).parent / 'images/green_check.png'
        green_check = logo_check(path)
        sub_col[1].write(f"{integrator_name}  {green_check}", unsafe_allow_html=True)
    else:
        sub_col[1].write(integrator_name)

    return option
       
        
# Integrator Connexion
def show_connection_expander(integrator_name, integrator_web_link):
    # Check if integrator activation is requested
    if st.session_state[f'activate_{integrator_name}'] == DEFAULT_STATUS:
        
        # Display connection expander
        with st.expander(f"{integrator_name} Connection", expanded=True):
            # Enter identifier
            api_key = st.text_input("Api key:", key=f"{integrator_name}_key")
            pc_function = getattr(pc, f"set{integrator_name}ApiKey")
            pc_function(api_key)
            login = st.button("Log in", key=f"{integrator_name}_connect")
            st.markdown(f"[Request api access key.]({integrator_web_link})")

            # Connect button handling
            if login:
                # Check identifier
                if pc.check(**{integrator_name: True}):
                    st.success(f"Connection successful with the api key: {api_key}")
                    # Save identifier
                    st.session_state[f'{integrator_name}_api_key'] = api_key
                    st.session_state[f'activate_{integrator_name}'] = INIT_STATUS
                    return 1
                else:
                    st.warning(f"{integrator_name} api key is incorrect.")
                
    return 0
            

def display_price(dataframe, label, drop_input_smiles = False):
    filename = f"{st.session_state.input_smiles}_{label.lower()}.csv"
    col = st.columns([3, 5.7, 1.3])
    string = label.replace('_', ' ') + " :"
    col[0].subheader(string)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        file_path = temp_file.name
        dataframe.to_csv(file_path, index=False)
        col[2].download_button(label="Download", data=open(file_path, 'rb').read(), file_name=filename)
        
    os.remove(file_path)
    
    dataframe = dataframe.dropna(axis=1, how='all')
    if drop_input_smiles:
        dataframe.drop("Input SMILES", axis=1, inplace=True)
    st.write(dataframe)
    st.write("")


def collect(smiles_df, progress_output):
    # Modifier cette fonction en fonction de votre utilisation réelle
    result = pc.collect(smiles_df, progress_output)
    st.session_state.result = result

######################
# CHEMICAL PRICE SEARCH
######################

def main():
    

    home1.title("ChemPrice: A Tool For Chemical Price Research")
    with home1.expander("About ChemPrice"):
        # Enter identifier
        st.write("ChemPrice is a Python tool for connecting to molecule sales platforms via API keys. The aim: automated extraction of data, such as prices and vendor names. ChemPrice supports Molport, ChemSpace and MCule integrators. It works by taking as input a list of molecules in the form of SMILES, producing a complete dataframe presenting all the prices found on different sources, as well as a second dataframe, highlighting the most advantageous offers in terms of quality/price ratio.")
        documentation_url = "https://differ-chemprice.readthedocs-hosted.com/en/latest/"
        st.markdown(f"If you are intrested in a more detailed explanation about ChemPlot please visit the official library's documentation at [Read the docs.]({documentation_url})")
        
    path = Path(__file__).parent / 'images/background.jpg'
    set_background(path)
    path = Path(__file__).parent / 'images/logo_chemprice.png'
    st.sidebar.markdown(logo_chemprice(path), unsafe_allow_html=True)
    st.sidebar.markdown("")


    ######################
    # CREATE A SECTION TO DISPLAY THE RESEARCH BAR
    ######################

    # You can add additional elements here
    home1.write("Input SMILES:")

    screen_division = home1.columns([1.3,5.7,1.7,1.3])
    
    home1.write("")


    ######################
    # Website choice
    ######################
    
    col = home1.columns(NB_INTEGRATORS + 1)

    # Première colonne : texte
    col[0].write("Select Integrators:")

    # Define integrators
    integrators = [
        ("Molport", "https://www.molport.com/shop/user-api-keys", 1),
        ("ChemSpace", "https://chem-space.com/contacts", 2),
        ("MCule", "https://mcule.com/contact/", 3),
    ]
    
    for integrator_name, integrator_web_link, integrator_num in integrators:
        initialize_integrator(integrator_name)

    selected_options = []
    option = {}
    # Create integrator checkbox
    refresh = 0
    for integrator_name, integrator_web_link, integrator_num in integrators:
        option[integrator_num] = create_integration_column(col[integrator_num], integrator_name)
        
        # Integrator connexion
        if option[integrator_num]:
            selected_options.append(integrator_name)
            if show_connection_expander(integrator_name, integrator_web_link):
                # If a connection with an integrator has been established, 
                # the page must be restarted to close the expander.
                refresh = 1
        
    ######################
    # COMMENTS
    ######################
    
    if not st.session_state["new_page"]:
        st.write("")
        
        st.markdown(
            """
            To use this interface, please follow these steps:
            1. In the search bar, either select a SMILES (Simplified Molecular Input Line Entry System) or import a CSV file containing the SMILES you are looking for (ensure that the SMILES are in the first column of the file).
            2. Choose the integrators you want to use.
            3. Click on the 'Search Prices' button to initiate the search.
            """
        )
      
    
    ######################
    # CSV UPLOAD
    ######################
    
    smiles_df = [] 
    if not st.session_state["new_page"]:
        smiles_file = st.sidebar.file_uploader("Choose a file", help = "The file must be a csv file with the list of SMILES to be searched in the first column.")

        if smiles_file is not None:
            df = pd.read_csv(smiles_file)
            if len(df) > LIMIT_SMILES:    # uncomment to limit the number of smiles displayed
               df = df[:LIMIT_SMILES]
               st.info("The file is too large, only the first 100 smiles are kept.")
               
            st.session_state.smiles_list = df.iloc[:, 0].to_list()
            st.session_state.input_smiles = st.session_state.smiles_list[0]
            smiles_df = st.session_state.smiles_list
        else:
            st.session_state.smiles_list = ""
        

    ######################
    # SEARCH BAR
    ######################     
        
    if bool(smiles_df):
        screen_division[1].write('*Search* *for* *SMILES* *from* *the* *file.* ')
    else:
        # Champ de saisie Streamlit avec placeholder
        st.session_state.input_smiles = screen_division[1].text_input(
            label="Enter a SMILES",
            value="",
            key="input_key",
            placeholder="Enter a SMILES : CC(=O)NC1=CC=C(C=C1)O",
            label_visibility="collapsed"
        )
        smiles_df = st.session_state.input_smiles

    
    ######################
    # SAVE THE IDENTIFIER INTO THE CLASS
    ######################
    
    if "Molport" in selected_options:
        if 'molport_username' in st.session_state and 'molport_password' in st.session_state:
            pc.setMolportUsername(st.session_state.molport_username)
            pc.setMolportPassword(st.session_state.molport_password)
    
        if 'Molport_api_key' in st.session_state:
            pc.setMolportApiKey(st.session_state['Molport_api_key'])
    
    if "ChemSpace" in selected_options:
        if 'ChemSpace_api_key' in st.session_state:
            pc.setChemSpaceApiKey(st.session_state['ChemSpace_api_key'])
    
    if "MCule" in selected_options:
        if 'MCule_api_key' in st.session_state:
            pc.setMCuleApiKey(st.session_state['MCule_api_key'])
    
    check_integrator = pc.check()
    if not selected_options:
        check_integrator = 0

        
    ######################
    # SEARCH PRICES
    ######################

    # Search button
    screen_division[2].button("Search Prices", key=2, on_click=but_click,args=([check_integrator]))
        
    # Search prices
    if st.session_state["new_page"]:
        
        if 'smiles_list' in st.session_state:
            smiles_df = st.session_state.smiles_list
            
        emptycont.empty()
        
        if bool(smiles_df):
            smiles_list = smiles_df
        else:
            smiles_list = [st.session_state.input_smiles]
            

        ######################
        # PROGRESS BAR
        ######################
        
        emptycont2 = st.empty()
        home2 = emptycont2.container()

        progress_output = []
        
        thread = threading.Thread(target=collect, args=(smiles_list, progress_output,))
        add_script_run_ctx(thread)
        thread.start()

        home2.text("Loading...")
        progress = 0.01
        progress_bar = home2.progress(0.0)  # Initialize the progress bar
        while not progress_output or progress_output[-1] < 1.0:
            if progress_output:
                if progress < progress_output[-1]:
                    progress = progress_output[-1]
            if progress < (1 - 0.00015):
                progress += 0.00014
            progress_bar.progress(progress)  # Update the progress bar
            
            time.sleep(0.1)  # Update the UI every 100ms

        home2.success("Progress completed.")
        
        emptycont2.empty()
        
        time.sleep(1)
        # Afficher le résultat
        all_prices = pd.DataFrame([])
        if not st.session_state.result.empty:
            all_prices = st.session_state.result
            
        best_prices = pc.selectBest(all_prices)
        
        
        ######################
        # RESULTS
        ######################
        
        st.sidebar.button(":house: Homepage", on_click=back_fun)

        if bool(smiles_df):
            smiles_with_price = all_prices.loc[all_prices['Price_USD'].notnull(), 'Input SMILES'].nunique()
            st.header(f"Result: {len(all_prices)} prices for {smiles_with_price} molecules are found.")

            if all_prices.empty: 
                st.write("No price found for this molecules.")
            else:
                # Utilisation de la fonction pour créer les boutons et afficher les données
                display_price(all_prices, "All_prices")
                display_price(best_prices, "Best_prices")

        else:
            st.header(f'Result for: {st.session_state.input_smiles}')
            
            if all_prices.empty: 
                st.write("No price found for this molecule.")
            else:
                # Utilisation de la fonction pour créer les boutons et afficher les données
                display_price(all_prices, "All_prices", drop_input_smiles=True)
                display_price(best_prices, "Best_prices", drop_input_smiles=True)

        st.session_state.smiles_list = ""
        
    if refresh:
        st.experimental_rerun()
        
if __name__ == "__main__":
    main()