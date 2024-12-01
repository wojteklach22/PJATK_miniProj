import pandas as pd
import numpy as np
import os

class AnalizeData:
    def __init__(self, filename):
        self.data = pd.read_csv(filename, delimiter=',')
        self.df = pd.DataFrame(self.data)
        if 'type_of_meat' in self.df.columns:
            self.df['type_of_meat'] = self.df['type_of_meat'].str.split(';')

    def basic_parameters(self):
        price = self.df['price']
        mean_price = price.mean()
        min_price = price.min()
        median_price = np.median(price)
        max_price = price.max()
        dev_price = price.std()
        price_25_percentile = np.percentile(price, 25)
        price_75_percentile = np.percentile(price, 75)
        print("Mean price:       ", mean_price)
        print("Standard deviation:", dev_price)
        print("Minimum price:    ", min_price)
        print("Maximum price:    ", max_price)
        print("25th percentile:   ", price_25_percentile)
        print("Median:            ", median_price)
        print("75th percentile:   ", price_75_percentile)

        analysis = "Kilka podstawowych parametrów do analizy:\n"
        analysis += f"""
        Mean price:       {mean_price}
        Standard deviation: {dev_price}
        Minimum price:      {min_price}
        Maximum price:      {max_price}
        25th percentile:    {price_25_percentile}
        Median:             {median_price}
        75th percentile:    {price_75_percentile}
        """
        return analysis

    def meat_and_weight_analysis(self):
        analysis = ""
        if 'type_of_meat' in self.df.columns:
            meat_price_stats = self.df.explode('type_of_meat').groupby('type_of_meat')['price'].describe()
            analysis += "\nCena według rodzaju mięsa:\n"
            analysis += str(meat_price_stats)
            print("\nCena według rodzaju mięsa:")
            print(meat_price_stats)

        if 'weight' in self.df.columns:
            weight_price_stats = self.df.groupby('weight')['price'].describe()
            analysis += "\nCena według gramatury:\n"
            analysis += str(weight_price_stats)
            print("\nCena według gramatury:")
            print(weight_price_stats)

        return analysis

    def compare_file_with(self, file1, file2):
        df1 = pd.read_csv(file1, delimiter=',')
        df2 = pd.read_csv(file2, delimiter=',')

        if 'type_of_meat' in df1.columns and 'type_of_meat' in df2.columns:
            meat_file1 = df1['type_of_meat'].explode().nunique()
            meat_file2 = df2['type_of_meat'].explode().nunique()
            compare_analysis = f"\nLiczba różnych rodzajów mięsa w {file1}: {meat_file1}\nLiczba różnych rodzajów mięsa w {file2}: {meat_file2}\n"
            print(f"\nLiczba różnych rodzajów mięsa w {file1}: {meat_file1}")
            print(f"Liczba różnych rodzajów mięsa w {file2}: {meat_file2}")
            if meat_file1 > meat_file2:
                compare_analysis += f"Więcej rodzajów mięsa oferuje {file1}.\n"
                print(f"Więcej rodzajów mięsa oferuje {file1}.")
            elif meat_file1 < meat_file2:
                compare_analysis += f"Więcej rodzajów mięsa oferuje {file2}.\n"
                print(f"Więcej rodzajów mięsa oferuje {file2}.")
            else:
                compare_analysis += f"Oba pliki oferują taką samą liczbę różnych rodzajów mięsa.\n"
                print(f"Oba pliki oferują taką samą liczbę różnych rodzajów mięsa.")

        mean_price_file1 = df1['price'].mean()
        mean_price_file2 = df2['price'].mean()
        compare_analysis += f"\nŚrednia cena w {file1}: {mean_price_file1:.2f}\nŚrednia cena w {file2}: {mean_price_file2:.2f}\n"
        print(f"\nŚrednia cena w {file1}: {mean_price_file1:.2f}")
        print(f"Średnia cena w {file2}: {mean_price_file2:.2f}")
        if mean_price_file1 < mean_price_file2:
            compare_analysis += f"{file1} ma niższe średnie ceny.\n"
            print(f"{file1} ma niższe średnie ceny.")
        elif mean_price_file1 > mean_price_file2:
            compare_analysis += f"{file2} ma niższe średnie ceny.\n"
            print(f"{file2} ma niższe średnie ceny.")
        else:
            compare_analysis += "Oba pliki mają taką samą średnią cenę.\n"
            print("Oba pliki mają taką samą średnią cenę.")

        if 'weight' in df1.columns and 'weight' in df2.columns:
            weight_counts_file1 = df1['weight'].value_counts()
            weight_counts_file2 = df2['weight'].value_counts()
            compare_analysis += f"\nLiczba produktów według gramatury w {file1}:\n{weight_counts_file1}\n"
            compare_analysis += f"\nLiczba produktów według gramatury w {file2}:\n{weight_counts_file2}\n"
            print(f"\nLiczba produktów według gramatury w {file1}:")
            print(weight_counts_file1)
            print(f"\nLiczba produktów według gramatury w {file2}:")
            print(weight_counts_file2)

        return compare_analysis

    def save_analysis_to_file(self, analysis, filename):
        folder = 'AnalizeData'
        filepath = os.path.join(folder, filename)
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(analysis)
        print(f"Analiza została zapisana w pliku {filepath}")

    def save_comparison_to_file(self, comparison):
        folder = 'AnalizeData'
        filepath = os.path.join(folder, "CompareShops.txt")
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(comparison)
        print(f"Porównanie zostało zapisane w pliku {filepath}")