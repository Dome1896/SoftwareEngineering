class User:
    def __init__(self, username, password, userID = 0):
        self.username = username
        self.password = password
        self.userID = userID

        self.tableName = "User"
    
    def makeRequestBody(self):
        return {"username" : self.username, "password": self.password}
        