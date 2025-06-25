class LivreIndisponibleError(Exception):
    def __init__(self,message="Livre est deja emprunter"):
        super().__init__(message)

class QuotaEmpruntDepasseError(Exception):
    def __init__(self,message="tu emprunte plus de 3 livres donc tu deppase le quota possible"):
        super().__init__(message)

class MembreInexistantError(Exception):
    def __init__(self,message="membre inexistant dans le fichier"):
        super().__init__(message)

class LivreInexistantError(Exception):
    def __init__(self,message="Livre inexistant dans le fichier "):
        super().__init__(message)

