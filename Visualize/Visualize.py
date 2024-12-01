import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class Visualize:
    def __init__(self, file1, file2):
        self.df1 = pd.read_csv(file1)
        self.df2 = pd.read_csv(file2)

    def compare_mean_price_for_popular_weight(self):
        popular_weight1 = self.df1['weight'].mode()[0]
        popular_weight2 = self.df2['weight'].mode()[0]

        df1_filtered = self.df1[self.df1['weight'] == popular_weight1]
        df2_filtered = self.df2[self.df2['weight'] == popular_weight2]

        mean_price1 = df1_filtered['price'].mean()
        mean_price2 = df2_filtered['price'].mean()

        labels = ['Zookarina', 'Zooexpress']
        mean_prices = [mean_price1, mean_price2]

        plt.figure(figsize=(8, 6))
        plt.bar(labels, mean_prices, color=['blue', 'orange'])
        plt.title('Porównanie średnich cen dla najpopularniejszej gramatury')
        plt.ylabel('Średnia cena (PLN)')
        plt.show()

    def plot_pie_or_histogram_for_meat_types(self):
        meat_types1 = self.df1['type_of_meat'].dropna().explode().value_counts()
        meat_types2 = self.df2['type_of_meat'].dropna().explode().value_counts()

        plt.figure(figsize=(10, 8))
        plt.subplot(1, 2, 1)
        meat_types1.plot.pie(autopct='%1.1f%%', startangle=90, title="Rozkład typów mięsa w Zookarina")
        plt.subplot(1, 2, 2)
        meat_types2.plot.pie(autopct='%1.1f%%', startangle=90, title="Rozkład typów mięsa w Zooexpress")
        plt.show()

    def plot_heatmap_for_meat_and_price(self):
        self.df1['meats'] = self.df1['type_of_meat'].dropna().apply(lambda x: x.split(';')).explode().reset_index(drop=True)
        self.df2['meats'] = self.df2['type_of_meat'].dropna().apply(lambda x: x.split(';')).explode().reset_index(drop=True)

        meat_price_df1 = self.df1.groupby('meats')['price'].mean()
        meat_price_df2 = self.df2.groupby('meats')['price'].mean()

        meat_price_comparison = pd.DataFrame({
            'Zookarina': meat_price_df1,
            'Zooexpress': meat_price_df2
        }).fillna(0)

        plt.figure(figsize=(12, 8))
        sns.heatmap(meat_price_comparison, annot=True, cmap='coolwarm', cbar=True, fmt=".2f")
        plt.title('Porównanie średnich cen rodzajów mięsa w sklepach')
        plt.ylabel('Rodzaje mięsa')
        plt.show()

