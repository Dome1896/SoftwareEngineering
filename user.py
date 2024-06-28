class User:
    '''
    Klasse, welche einen User darstellt
    '''
    def __init__(self, username:str, password:str, userID:str = "0"):
        '''
        Initialisierung der Klasse User
        :param username: Username des Users
        :param password: Passwort des Users
        :param userID: ID des Users -> Standard ist 0
        '''
        self.username = username
        self.password = password
        self.userID = userID

        self.tableName = "User"
    
    def makeRequestBody(self):
        '''
        Erstellt den Request Body für die Datenbank
        :return: Request Body
        '''
        return {"username" : self.username, "password": self.password}
        