from .user import User
import json

class LibUser:
    
    def login(self, email, password):
        file = open('data/users.json')
        j = json.load(file)
        for x in j:
            if x['email'] == email and x['password'] == password:
                return True
        return False

    def create(self, email, password, nombre, apellido):
        user = User(email, password, nombre, apellido)
        file = open("data/users.json")
        j = json.load(file)
        j = j + [user.toJson()]
        file = open("data/users.json", "w")
        json.dump(j, file, ensure_ascii=False, indent=4)
        file.close()
        return True

    def get_users(self):
        file = open("data/users.json")
        j = json.load(file)
        list = []
        for x in j:
            list.append(User(x['email'], x['password'], x['nombre'], x['apellido']))
        return list 

    def get_user_by_email(self, email):
        file = open("data/users.json")
        j = json.load(file)
        for x in j: 
            if(x['email']==email):
                return User(x['email'],x['password'],x['nombre'],x['apellido'])
        return None

    def edit_user(self, email, password, nombre, apellido):
        file = open("data/users.json")
        j = json.load(file)
        for x in j: 
            if(x['email']==email):
                x['email'] = email
                x['password']= password
                x['nombre']= nombre
                x['apellido']= apellido
                file = open("data/users.json","w")
                json.dump(j,file,ensure_ascii=False, indent=4)
                file.close()
                return True
        return False

    def eliminar(self, email):
        file = open("data/users.json")
        j = json.load(file)
        for i in range(0, len(j)):
            if j[i]['email'] == email:
                j = j[:i] + j[i+1:]
                file = open("data/users.json", "w")
                json.dump(j, file, ensure_ascii=False, indent=4)
                file.close()
                return True
        return False
