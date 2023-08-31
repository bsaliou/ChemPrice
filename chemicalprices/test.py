import chemicalprices as cp

# "paracetamol, ibuprofène, aspirin"
smiles_list = ["CC(=O)NC1=CC=C(C=C1)O", "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", "O=C(C)Oc1ccccc1C(=O)O"]

pc = cp.PriceCollector()

pc.setMolportApiKey("880d8343-8ui2-418c-9g7a-68b4e2e78c8b")
pc.setChemSpaceApiKey("NS1mN3f2Gw-3qXsQIztj_E6MPNQudCc_EZGQ9hlzzodVWF1McK6l6o-VAdB5t5X2")
pc.setMCuleApiKey("9a37d3d8c1ee3546ddb107f3d189e86e1f61418e")

pc.status() # print activated integrators
pc.check() # make single request from activated integrators , print if the request returns correctly

all_prices = pc.collect(smiles_list)
best_prices = pc.selectBest(all_prices)
best_prices.to_csv("price.csv")