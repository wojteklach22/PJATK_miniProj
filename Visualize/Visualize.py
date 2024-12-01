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

    def pie_chart(self):
        def check_for_less_than_one(series):
            # Avoid to many names on the chart, group by less than 1%
            percentages = series / series.sum() * 100
            less_than_one = percentages[percentages < 1].index
            other_sum = series.loc[less_than_one].sum()
            series = series.drop(less_than_one)
            series['inne'] = other_sum
            return series

        meat_types1 = self.df1['type_of_meat'].dropna().apply(lambda x: x.split(';')).explode().value_counts()
        meat_types2 = self.df2['type_of_meat'].dropna().apply(lambda x: x.split(';')).explode().value_counts()

        meat_types1 = check_for_less_than_one(meat_types1)
        meat_types2 = check_for_less_than_one(meat_types2)

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        meat_types1.plot.pie(autopct='%1.1f%%', startangle=90, title="Rozkład typów mięsa w Zookarina")
        plt.ylabel("")
        plt.subplot(1, 2, 2)
        meat_types2.plot.pie(autopct='%1.1f%%', startangle=90, title="Rozkład typów mięsa w Zooexpress")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()

    def heatmap(self):
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

