class User: 
    def __init__(self,email,password, nombre, apellido):
        self.email = email
        self.password = password
        self.nombre = nombre
        self.apellido = apellido
    
    def toJson(self):
        return {'email':self.email, 'password':self.password, 'nombre':self.nombre , 'apellido':self.apellido}