class Password:
    def __init__(self, identifier='', email='', hash='', password='', dump=''):
        if identifier == '' and email != '':
            self.identifier = email
        else:
            self.identifier = identifier
        self.email = email
        self.hash = hash
        self.password = password
        self.dump = dump

    def tuple(self):
        return (self.identifier, self.email, self.hash, self.password,
                self.dump)
