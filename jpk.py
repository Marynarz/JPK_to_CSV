import csv
import xml.etree.ElementTree as ET
from dataclasses import dataclass

prefix_map = {
    "etd": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2016/01/25/eD/DefinicjeTypy/",
    "tns": "http://jpk.mf.gov.pl/wzor/2016/03/09/03093/",
}


@dataclass
class Document_JPK:
    NumerPZ: str
    DataPZ: str
    WartoscPZ: str
    DataOtrzymania_PZ: str
    Dostawca: str
    NumerFaPZ: str

    def __str__(self):
        return "Numer: {}\t Data: {}\t Wartosc: {}\t Data otrzymania: {}\t Dostawca: {}\t Numer FV: {}".format(
            self.NumerPZ,
            self.DataPZ,
            self.WartoscPZ,
            self.DataOtrzymania_PZ,
            self.Dostawca,
            self.NumerFaPZ,
        )

    def __iter__(self):
        return iter(
            [
                self.NumerPZ,
                self.DataPZ,
                self.WartoscPZ,
                self.DataOtrzymania_PZ,
                self.Dostawca,
                self.NumerFaPZ,
            ]
        )


records = [
    Document_JPK("Numer", "Data", "Wartosc", "Data otrzymania", "Dostawca", "Numer FV")
]


def parseXML(xmlfile):
    tree = ET.parse(xmlfile)

    root = tree.getroot()

    store = root.find(".//tns:Magazyn", prefix_map).text
    print("Magazyn: {}".format(store))

    for pz_header in root.findall(".//tns:PZ", prefix_map):
        for pz_value in pz_header.findall(".//tns:PZWartosc", prefix_map):
            doc = Document_JPK(
                NumerPZ=pz_value.find(".//tns:NumerPZ", prefix_map).text,
                DataPZ=pz_value.find(".//tns:DataPZ", prefix_map).text,
                WartoscPZ=pz_value.find(".//tns:WartoscPZ", prefix_map).text,
                DataOtrzymania_PZ=pz_value.find(
                    ".//tns:DataOtrzymaniaPZ", prefix_map
                ).text,
                Dostawca=pz_value.find(".//tns:Dostawca", prefix_map).text,
                NumerFaPZ=(
                    pz_value.find(".//tns:NumerFaPZ", prefix_map).text
                    if pz_value.find(".//tns:NumerFaPZ", prefix_map) is not None
                    else ""
                ),
            )
            records.append(doc)

    for wz_header in root.findall(".//tns:WZ", prefix_map):
        for wz_value in wz_header.findall(".//tns:WZWartosc", prefix_map):
            doc = Document_JPK(
                NumerPZ=wz_value.find(".//tns:NumerWZ", prefix_map).text,
                DataPZ=wz_value.find(".//tns:DataWZ", prefix_map).text,
                WartoscPZ=wz_value.find(".//tns:WartoscWZ", prefix_map).text,
                DataOtrzymania_PZ=wz_value.find(
                    ".//tns:DataWydaniaWZ", prefix_map
                ).text,
                Dostawca="",
                NumerFaPZ="",
            )
            records.append(doc)

    for rw_header in root.findall(".//tns:RW", prefix_map):
        for rw_value in rw_header.findall(".//tns:RWWartosc", prefix_map):
            doc = Document_JPK(
                NumerPZ=rw_value.find(".//tns:NumerRW", prefix_map).text,
                DataPZ=rw_value.find(".//tns:DataRW", prefix_map).text,
                WartoscPZ=rw_value.find(".//tns:WartoscRW", prefix_map).text,
                DataOtrzymania_PZ=rw_value.find(
                    ".//tns:DataWydaniaRW", prefix_map
                ).text,
                Dostawca="",
                NumerFaPZ="",
            )
            records.append(doc)

    print("Znaleziono:")
    for record in records:
        print(record)


def generate_csv(filename="dokumenty.csv"):
    print("\nGenerowanie pliku csv: {}".format(filename))
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile, dialect="excel")
        writer.writerows(records)
    print("Wygenerowano: {}".format(filename))


def main():
    parseXML("test.xml")
    generate_csv()


if __name__ == "__main__":
    main()
