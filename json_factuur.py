import json
import os 
from shutil import move
from datetime import datetime
def process_factur(filename:str):
    try:
        with open('JSON_ORDER/'+filename, "r") as file:
            order_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error by processing {filename}: {e}")
        return
    order = order_data["order"]

    invoice = {
        "factuurnummer": f"INV-{order['ordernummer']}",
        "factuurdatum": datetime.today().strftime("%d-%m-%Y"),
        "vervaldatum": (datetime.today()).strftime("%d-%m-%Y"), 
        "klant": order["klant"],
        "producten": [],
        "totaal_excl_btw": 0,
        "totaal_btw": 0,
        "totaal_incl_btw": 0
    }

    for product in order["producten"]:
        subtotaal_excl = product["aantal"] * product["prijs_per_stuk_excl_btw"]
        btw_bedrag = round(subtotaal_excl * (product["btw_percentage"] / 100), 2)
        subtotaal_incl = subtotaal_excl + btw_bedrag
        
        invoice["producten"].append({
            "productnaam": product["productnaam"],
            "aantal": product["aantal"],
            "prijs_per_stuk_excl_btw": product["prijs_per_stuk_excl_btw"],
            "btw_percentage": product["btw_percentage"],
            "subtotaal_excl_btw": subtotaal_excl,
            "btw_bedrag": btw_bedrag,
            "subtotaal_incl_btw": subtotaal_incl
        })
        
        invoice["totaal_excl_btw"] += subtotaal_excl
        invoice["totaal_btw"] += btw_bedrag
        invoice["totaal_incl_btw"] += subtotaal_incl

    factuur_path=os.path.join('JSON_INVOICE','factuur_'+filename)
    with open(factuur_path, "w") as file:
        json.dump(invoice, file, indent=4)
    move('JSON_ORDER/'+filename,'JSON_PROCESSED')
for filename in os.listdir('JSON_ORDER'):
    process_factur(filename)