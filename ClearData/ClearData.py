import re
import pandas as pd

class ClearData:
    def __init__(self, filename):
        self.data = pd.read_csv(filename, delimiter=',')
        self.df = pd.DataFrame(self.data)

    def cleaning_data(self, output_file):
        self.df['price'] = self.df['price'].str.replace(r'[^\d,]', '', regex=True)  # Only numeric value
        self.df['price'] = self.df['price'].str.replace(r'"', '', regex=True)  # Delete "" from price
        self.df['price'] = pd.to_numeric(self.df['price'].str.replace(r',', '.', regex=True))  # replace , by .

        meat_keywords = {
            "kurczak": ["kurczak", "chicken", "kury", "kura", "kur"],
            "ryba": ["ryba", "fish", "ryb"],
            "łosoś": ["łosoś", "salmon", "łoso", "loso"],
            "tuńczyk": ["tuńczyk", "tuna", "tuń"],
            "indyk": ["indyk", "turkey", "indy"],
            "krewetka": ["krewetka", "shrimp", "krewet"],
            "renifer": ["renifer", "reindeer", "renife"],
            "kaczka": ["kaczka", "duck", "kacz"],
            "wątróbka": ["wątróbka", "liver", "watrobka", "wątrób", "watrob"],
            "jagnięcina": ["jagnięcina", "lamb", "jagniecina", "jagnięc", "jagniec"],
            "wołowina": ["wołowina", "beef", "wolowina", "wołowi", "wolowi"],
            "dorsz": ["dorsz", "cod", "dors"],
            "sardynki": ["sardynki", "sardines", "sardyn"],
            "pstrąg": ["pstrąg", "trout", "pstrag", "pstr"],
            "królik": ["królik", "rabbit", "krolik", "król", "krol"],
            "okoń": ["okoń", "perch", "okon"],
            "dziczyzna": ["dziczyzna", "venison", "dziczyz"],
            "drób": ["drób", "drobiowy", "poultry", "drob"],
            "sarnina": ["sarnina", "roe", "sarni"],
            "cielęcina": ["cielęcina", "veal", "cielecina", "ciele"],
            "krab": ["krabem", "crab", "krab"]
        }

        def detect_meat_type(name):
            detected_meats = []
            for meat, keywords in meat_keywords.items():
                if any(keyword.lower() in name.lower() for keyword in keywords):
                    detected_meats.append(meat)
            return "; ".join(detected_meats) if detected_meats else "Mix"

        self.df['type_of_meat'] = self.df['name'].apply(detect_meat_type)

        def extract_weight_of_product(name):
            single_weight = re.search(r'(\d+)\s?g', name.lower())  # 85g case
            multi_weight = re.search(r'(\d+)\s?x\s?(\d+)\s?g', name.lower())  # 4x85g case

            if multi_weight:
                count, weight = map(int, multi_weight.groups())
                return count * weight
            elif single_weight:
                return int(single_weight.group(1))
            else:
                return None

        self.df['weight'] = pd.to_numeric(self.df['name'].apply(extract_weight_of_product))

        self.df.to_csv(output_file, index=False, encoding="utf-8-sig")