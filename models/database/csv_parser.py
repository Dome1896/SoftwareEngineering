import csv
from models.card.card import Card
from io import StringIO

class CSVParser():
    def __init__(self, file_path = None):
        self.file_path = file_path

    def create_card_object_list(self, owner_id):

        card_list = []
        with open(self.file_path, mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                card_list.append(Card(category=line[0],
                                      question=line[1], 
                                      answer=line[2],
                                      ownerID=owner_id))
                
        return card_list
    
    def create_csv_string_from_cards(self, card_list):
        data_list = []
        for card in card_list:
            data_list.append([card.category, card.question, card.answer])
        csv_string = self.__list_to_csv(data_list)
        return csv_string


    def __list_to_csv(self, objekt_liste, header=None):
        """
        Konvertiert eine Liste von Objekten in einen CSV-String.
        
        :param objekt_liste: Liste von Objekten (z. B. Wörterbücher oder Listen).
        :param header: Optional, eine Liste mit Spaltennamen (z. B. ["Name", "Alter", "Stadt"]).
        :return: Ein CSV-String mit den Daten.
        """
        output = StringIO()
        writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Header schreiben, falls angegeben
        if header:
            writer.writerow(header)
        
        # Daten schreiben
        for obj in objekt_liste:
            # Prüfen, ob das Objekt ein Wörterbuch oder eine Liste ist
            if isinstance(obj, dict) and header:
                # Werte aus dem Wörterbuch in der Reihenfolge des Headers extrahieren
                writer.writerow([obj.get(key, "") for key in header])
            elif isinstance(obj, (list, tuple)):
                # Direkt schreiben, falls es eine Liste oder ein Tuple ist
                writer.writerow(obj)
            else:
                raise ValueError("Die Liste muss aus Wörterbüchern oder Listen/Tuples bestehen.")

        return output.getvalue()