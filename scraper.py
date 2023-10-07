import requests
import csv
from bs4 import BeautifulSoup

class NOAAScraper:
    def __init__(self):
        self.base_url = "https://www.nnvl.noaa.gov/view/globaldata.html"

    def fetch_datasets(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            dataset_elements = soup.find_all("div", class_="dataset")
            datasets = []

            for element in dataset_elements:
                dataset = {}
                dataset["Name"] = element.find("h3").text.strip()
                dataset["Description"] = element.find("p").text.strip()
                datasets.append(dataset)

            return datasets
        else:
            print("Failed to fetch data. Status code:", response.status_code)
            return []

    def export_to_csv(self, datasets, filename="noaa_datasets.csv"):
        if datasets:
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                fieldnames = ["Name", "Description"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for dataset in datasets:
                    writer.writerow(dataset)
            print(f"Data exported to {filename}")

if __name__ == "__main__":
    noaa_scraper = NOAAScraper()
    datasets = noaa_scraper.fetch_datasets()
    noaa_scraper.export_to_csv(datasets)
