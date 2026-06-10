from datetime import datetime

LOG_FILE = "chansons.log"

def ecrire_log(nom_programme: str, message: str):
    """
    Prend le nom du programme et le message en paramètre,
    puis formate le log de manière identifiable.
    """
    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # On ajoute [NOM_PROG] juste après la date pour bien aligner le tout
    ligne_log = f"[{horodatage}] [{nom_programme.upper()}] {message}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(ligne_log)