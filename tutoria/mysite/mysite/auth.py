import json
import os

class AuthManager:
    def __init__(self, file_path='usuarios.json'):
        self.file_path = file_path
    
    def _load_users(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def authenticate(self, email, password):
        users = self._load_users()
        return any(u['email'] == email and u['password'] == password for u in users)