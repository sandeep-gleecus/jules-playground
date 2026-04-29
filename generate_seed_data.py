import json
import uuid
import random
from datetime import datetime, timezone, timedelta

def escape_sql_string(s):
    if s is None:
        return "NULL"
    if isinstance(s, dict):
        s = json.dumps(s)
    # Double single quotes to escape them in SQL
    return "'" + str(s).replace("'", "''") + "'"

def escape_sql_array(arr):
    if arr is None:
        return "NULL"
    # Convert list to postgres array syntax '{a,b}'
    inner = ",".join(arr)
    return f"'{'{'}{inner}{'}'}'"

def escape_sql_value(v):
    if v is None or v == "":
        return "NULL"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, bool):
        return "true" if v else "false"
    return escape_sql_string(v)

def generate_seed_data(num_products=10, filename="seed_data.sql"):
    brands = ["CoolBrand", "TechGlow", "EcoAppliance", "HomeSmart", "QuantumGoods"]
    categories = ["Appliances", "Electronics", "Furniture"]
    sub_categories = ["Refrigerators", "Washing Machines", "Microwaves", "Laptops", "Televisions"]
    statuses = ["ACTIVE", "INACTIVE", "ARCHIVED"]
    types = ["SmallWhiteGoods", "LargeWhiteGoods", "ConsumerElectronics"]
    goods_types = ["SMALL_WHITE_GOODS", "LARGE_WHITE_GOODS", "CONSUMER_ELECTRONICS"]
    complexities = ["LOW", "MEDIUM", "HIGH"]
    certifications = ["epr", "iso", "spcb", "rohs", "weee"]
    haz_materials = ["refrigerant_r134a", "lithium_ion", "lead", "mercury"]

    component_names = ["Compressor", "Motor", "Circuit Board", "Display Panel", "Casing", "Power Supply", "Cooling Fan"]
    component_types = ["Mechanical", "Electrical", "Electronic", "Structural"]
    uoms = ["each", "kg", "g", "cm"]

    material_names = ["Steel Body", "Copper Wire", "Aluminum Frame", "Plastic Cover", "Glass Screen", "Silicon Chip"]
    material_codes = ["ST", "CU", "AL", "PL", "GL", "SI"]
    material_categories = ["Metal", "Plastic", "Glass", "Composite"]

    product_id_counter = 1
    component_id_counter = 1
    material_id_counter = 1

    with open(filename, "w", encoding="utf-8") as f:
        f.write("-- Seed Data Generation\n\n")

        for _ in range(num_products):
            # Generate Product
            prod_uuid = str(uuid.uuid4())
            brand = random.choice(brands)
            manufacturer_json = {
                "oem": str(uuid.uuid4()),
                "origin": random.choice(["South Korea", "China", "USA", "Germany", "Japan"]),
                "facility": f"{random.choice(['Seoul', 'Shenzhen', 'Austin', 'Berlin', 'Tokyo'])} Plant"
            }

            market_value_json = {
                "avg_sale_time": f"{random.randint(10, 60)} days",
                "disposal_cost": round(random.uniform(5.0, 50.0), 2),
                "market_demand": random.choice(["low", "medium", "high"]),
                "location_context": random.choice(["APAC", "NA", "EMEA"]),
                "total_parts_value": round(random.uniform(50.0, 200.0), 2),
                "net_recycling_value": round(random.uniform(10.0, 100.0), 2),
                "valuation_timestamp": "2026-01-01T00:00:00Z",
                "current_market_value": round(random.uniform(100.0, 500.0), 2),
                "total_recycling_value": round(random.uniform(20.0, 150.0), 2),
                "net_parts_harvest_value": round(random.uniform(40.0, 150.0), 2),
                "estimated_refurbish_cost": round(random.uniform(20.0, 100.0), 2),
                "refurbished_market_value": round(random.uniform(150.0, 600.0), 2),
                "expected_refurbish_profit": round(random.uniform(50.0, 300.0), 2)
            }

            market_value_avgs_json = {
                "avg_baseline_cost": round(random.uniform(100.0, 300.0), 2),
                "avg_scrap_net_cost": round(random.uniform(5.0, 20.0), 2),
                "avg_harvest_net_cost": round(random.uniform(10.0, 50.0), 2),
                "avg_refurbish_net_cost": round(random.uniform(30.0, 100.0), 2),
                "avg_diverted_scrap_weight": round(random.uniform(1.0, 10.0), 2),
                "avg_diverted_harvest_weight": round(random.uniform(5.0, 20.0), 2),
                "avg_diverted_refurbish_weight": round(random.uniform(10.0, 50.0), 2),
                "avg_material_weight_recovered": round(random.uniform(5.0, 30.0), 2),
                "avg_component_weight_recovered": round(random.uniform(10.0, 40.0), 2)
            }

            created_at = datetime.now(timezone.utc).isoformat()
            req_certs = random.sample(certifications, k=random.randint(1, 3))
            haz_mats = random.sample(haz_materials, k=random.randint(0, 2))

            f.write(f"INSERT INTO product_master (id, uuid, status, type, name, category, sub_category, brand, manufacturer, upc, variant, model_number, serial_number, model_year, weight_lb, weight_kg, dimensions_inches, repairability_score, disassembly_complexity, average_life_span_years, energy_efficiency_rating, authorized_needed, special_handling_required, contains_user_data, mandatory_data_wipe_needed, required_certifications, market_value, market_value_avgs, hazardous_materials, additional_data, created_at, updated_at, goods_type, master_uuid, gtin, ean) VALUES (")
            f.write(f"{product_id_counter}, {escape_sql_string(prod_uuid)}, {escape_sql_string(random.choice(statuses))}, {escape_sql_string(random.choice(types))}, {escape_sql_string(f'Product {product_id_counter}')}, {escape_sql_string(random.choice(categories))}, {escape_sql_string(random.choice(sub_categories))}, {escape_sql_string(brand)}, {escape_sql_string(manufacturer_json)}, {escape_sql_string('1' + str(random.randint(1000000000, 9999999999)))}, {escape_sql_string('Silver')}, {escape_sql_string(f'MOD-{product_id_counter}')}, '', {escape_sql_string(str(random.randint(2015, 2025)))}, {round(random.uniform(10.0, 100.0), 3)}, {round(random.uniform(5.0, 50.0), 3)}, {escape_sql_string('20 x 20 x 30')}, {round(random.uniform(1.0, 10.0), 2)}, {escape_sql_string(random.choice(complexities))}, {random.randint(5, 20)}, {escape_sql_string('A++')}, {random.choice(['true', 'false'])}, {random.choice(['true', 'false'])}, {random.choice(['true', 'false'])}, {random.choice(['true', 'false'])}, {escape_sql_array(req_certs)}, {escape_sql_string(market_value_json)}, {escape_sql_string(market_value_avgs_json)}, {escape_sql_array(haz_mats)}, {escape_sql_string({'source_data': 'seed'})}, {escape_sql_string(created_at)}, {escape_sql_string(created_at)}, {escape_sql_string(random.choice(goods_types))}, '', '', '');\n")

            num_components = random.randint(2, 5)
            selected_components = random.sample(component_names, num_components)
            for comp_name in selected_components:
                comp_uuid = str(uuid.uuid4())

                f.write(f"INSERT INTO product_components (id, uuid, product_id, parent_component_id, name, type, quantity, uom, weight_kg, carbon_factor, virgin_emission_factor, recycling_emission_factor, refurbish_emission_factor, reusability_score, recyclability_score, repairability_score, material_recovery_routes, recommended_action, created_at) VALUES (")
                f.write(f"{component_id_counter}, {escape_sql_string(comp_uuid)}, {product_id_counter}, NULL, {escape_sql_string(comp_name)}, {escape_sql_string(random.choice(component_types))}, {round(random.uniform(1.0, 5.0), 2)}, {escape_sql_string(random.choice(uoms))}, {round(random.uniform(0.5, 15.0), 3)}, {round(random.uniform(1.0, 5.0), 5)}, {round(random.uniform(2.0, 10.0), 5)}, {round(random.uniform(0.5, 3.0), 5)}, {round(random.uniform(0.8, 4.0), 5)}, {round(random.uniform(0.1, 1.0), 2)}, {round(random.uniform(0.1, 1.0), 2)}, {round(random.uniform(0.1, 1.0), 2)}, NULL, NULL, {escape_sql_string(created_at)});\n")

                num_materials = random.randint(1, 3)
                # create indices and names based on those indices
                mat_indices = random.sample(range(len(material_names)), num_materials)
                for mi in mat_indices:
                    mat_name = material_names[mi]
                    mat_code = material_codes[mi]
                    mat_cat = material_categories[mi % len(material_categories)]
                    mat_sys_id = f"MAT-{mat_code}-0{random.randint(1,9)}"

                    f.write(f"INSERT INTO product_materials (id, component_id, material_id, material_name, material_code, material_category, fraction_weight, created_at) VALUES (")
                    f.write(f"{material_id_counter}, {component_id_counter}, {escape_sql_string(mat_sys_id)}, {escape_sql_string(mat_name)}, {escape_sql_string(mat_code)}, {escape_sql_string(mat_cat)}, {round(random.uniform(5.0, 100.0), 2)}, {escape_sql_string(created_at)});\n")

                    material_id_counter += 1

                component_id_counter += 1

            product_id_counter += 1
            f.write("\n")

if __name__ == '__main__':
    generate_seed_data(10)
    print("Successfully generated seed_data.sql with 10 product records")
