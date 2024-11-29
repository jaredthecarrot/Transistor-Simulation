import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from mp_api.client import MPRester
import subprocess

API_KEY = "de7LQ33VXWmZDcTOzY1dLDxk8PqLoP4O"
LTSPICE_TEMPLATE_PATH = "ltspice_template.cir"
LTSPICE_OUTPUT_PATH = "generated_netlist.cir"
LTSPICE_EXE_PATH = r"C:\Users\jared\AppData\Local\Programs\ADI\LTspice\LTspice.exe"

def fetch_material_data(material_ids):
    with MPRester(API_KEY) as mpr:
        docs = mpr.materials.summary.search(
            material_ids=material_ids,
            fields=["material_id", "band_gap", "energy_above_hull"]
        )
        for doc in docs:
            print(f"Fetched data for {doc.material_id}: Band Gap = {doc.band_gap}, Energy Above Hull = {doc.energy_above_hull}")
        return [
            {
                "material_id": doc.material_id,
                "band_gap": doc.band_gap if doc.band_gap is not None else 0.0,
                "energy_above_hull": doc.energy_above_hull if doc.energy_above_hull is not None else 0.1,
            }
            for doc in docs
        ]

def map_properties_to_spice(material_properties):
    band_gap = material_properties["band_gap"]
    energy_above_hull = material_properties["energy_above_hull"]
    vto = band_gap * 0.7
    kp = max(1e-5, 1 / (1 + energy_above_hull))
    return {"VTO": vto, "KP": kp}

def generate_ltspice_netlist(template_path, output_path, spice_params):
    with open(template_path, "r") as template_file:
        netlist = template_file.read()
    for key, value in spice_params.items():
        netlist = netlist.replace(f"{{{key}}}", str(value))
    with open(output_path, "w") as output_file:
        output_file.write(netlist)
    print(f"Generated netlist saved to: {output_path}")

def run_ltspice_simulation(netlist_path):
    subprocess.run([LTSPICE_EXE_PATH, "-Run", netlist_path])
    print(f"LTSpice simulation completed for: {netlist_path}")

def screen_materials_with_rf(material_data):
    dataset = pd.DataFrame({
        "band_gap": [0.61, 0.00, 1.1, 1.5, 2.0, 0.8],
        "energy_above_hull": [0.000, 0.000, 0.005, 0.01, 0.02, 0.04],
        "suitable": [1, 1, 1, 0, 0, 0]
    })

    features = dataset[["band_gap", "energy_above_hull"]]
    labels = dataset["suitable"]

    classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    classifier.fit(features, labels)

    material_features = np.array([
        [material_data["band_gap"], material_data["energy_above_hull"]]
    ])
    prediction = classifier.predict(material_features)
    print(f"Material {material_data['material_id']} prediction: {'Suitable' if prediction[0] == 1 else 'Not Suitable'}")
    return prediction[0] == 1

def main():
    material_ids = ["mp-149", "mp-32", "mp-2348641"]
    materials = fetch_material_data(material_ids)

    for material in materials:
        print(f"Processing material: {material['material_id']}")
        
        is_suitable = screen_materials_with_rf(material)
        if not is_suitable:
            print(f"Material {material['material_id']} is not suitable for the transistor simulation.")
            continue

        spice_params = map_properties_to_spice(material)
        print(f"Mapped SPICE parameters for {material['material_id']}: {spice_params}")

        generate_ltspice_netlist(LTSPICE_TEMPLATE_PATH, LTSPICE_OUTPUT_PATH, spice_params)
        run_ltspice_simulation(LTSPICE_OUTPUT_PATH)

if __name__ == "__main__":
    main()
