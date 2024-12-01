from Data.GetValues1 import GetValues1
from Data.GetValues2 import GetValues2
from ClearData.ClearData import ClearData
from AnalizeData.AnalizeData import AnalizeData
from Visualize.Visualize import Visualize

def main():
    getvalues1 = GetValues1()
    products = getvalues1.fetch_all_products()
    getvalues1.save_to_csv(products, "Output/zookarinaproducts.csv")
    print(f"Pobrano {len(products)} produktów i zapisano do zookarinaproducts.csv")
    input_file = "Output/zookarinaproducts.csv"
    output_file = "Output/zookarinaproducts_cleaned.csv"
    cleaner = ClearData(input_file)
    cleaner.cleaning_data(output_file)
    print(f"Przetwarzanie zakończone! Wynik zapisano w {output_file}")
    analyzer = AnalizeData(output_file)
    basic_parameters = analyzer.basic_parameters()
    meat_and_weight_analysis = analyzer.meat_and_weight_analysis()
    analyzer.save_analysis_to_file(basic_parameters + meat_and_weight_analysis, "zookarina_analyze.txt")

    getvalues2 = GetValues2()
    products = getvalues2.fetch_all_products()
    getvalues2.save_to_csv(products, "Output/zooexpressproducts.csv")
    print(f"Pobrano {len(products)} produktów i zapisano do zooexpressproducts.csv")
    input_file = "Output/zooexpressproducts.csv"
    output_file = "Output/zooexpressproducts_cleaned.csv"
    cleaner = ClearData(input_file)
    cleaner.cleaning_data(output_file)
    print(f"Przetwarzanie zakończone! Wynik zapisano w {output_file}")
    analyzer = AnalizeData(output_file)
    basic_parameters = analyzer.basic_parameters()
    meat_and_weight_analysis = analyzer.meat_and_weight_analysis()
    analyzer.save_analysis_to_file(basic_parameters + meat_and_weight_analysis, "zooexpress_analyze.txt")

    # Compare both files
    file1 = "Output/zookarinaproducts_cleaned.csv"
    file2 = "Output/zooexpressproducts_cleaned.csv"
    comparison = analyzer.compare_file_with(file1, file2)
    analyzer.save_comparison_to_file(comparison)

    # Chart
    visualizer = Visualize(file1, file2)
    visualizer.compare_mean_price_for_popular_weight()
    visualizer.plot_pie_or_histogram_for_meat_types()
    visualizer.plot_heatmap_for_meat_and_price()


if __name__ == "__main__":
    main()
