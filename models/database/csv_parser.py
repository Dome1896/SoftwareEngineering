import csv
from models.card.card import Card
class CSVParser():
    def __init__(self, file_path):
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