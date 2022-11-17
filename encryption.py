
class Encryption:
    def __init__(self, path):
        self.path = path


    def create_key(self, password):


    def execute(self):
        with open(self.path, 'r') as file:
            data_to_encrypt = file.read()

        fernet = Fernet()