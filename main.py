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
    visualizer.pie_chart()
    visualizer.heatmap()


if __name__ == "__main__":
    main()


######################################################################################################################
################################################RAPORT################################################################
######################################################################################################################
# Analiza rozpoczęła się od pobrania danych ze stron internetowych, aby to zrobić na pierwszej z nich trzebabyło dodać
# kliknięcie przycisku akceptacji cookies oraz potem po pobraniu przejście na drugą stronę aby pobrać resztę danych, po
# czym dane zostały zapisane do pliku .csv. Dla drugiej strony trzeba było po wczytaniu danych zjechać scrolem na dół
# strony po czym przejśc na kolejną i tak aż do momentu pobrania 18 stron danych, również ich wynik został zapisany do
# pliku .csv. Następnie pliki zostały oczyszczone i przygotowane zostały dane wejściowe, zmienione separatory, rozdzielenie
# nazwy na gramaturę i rodzaj mięsa, poprawa zapisu ceny oraz transformacja ceny i wagi na postać numeryczną, po tym
# przeprowadzono analizy w ramach średniej ceny i popularności gramatury, oraz typ mięs i ich cena co zostało zapisane
# do 2 plików w formacie .txt oraz ostatniego w formacie .txt który posiadał porównanie 2 stron. Na sam koniec zostały
# stworzone 3 wykresy, które pozwoliły wizualnie zobrazować różnice między sklepami, które dokładniej zostały opisane
# w pliku README.md jako porównania, wnioski i spostrzeżenia.