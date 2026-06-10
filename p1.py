import os
from logs import ecrire_log

NOM_MODULE = "P1"

def recuperer_mp3(dossier: str) -> dict:
    mp3_trouves = {}
    
    if not os.path.exists(dossier):
        os.makedirs(dossier)
        ecrire_log(NOM_MODULE, f"Création du dossier surveillé : {os.path.abspath(dossier)}")
        
    for fichier in os.listdir(dossier):
        if fichier.lower().endswith('.mp3'):
            chemin_absolu = os.path.abspath(os.path.join(dossier, fichier))
            mp3_trouves[fichier] = chemin_absolu
            
    return mp3_trouves

def verifier_nouvelles_chansons(chansons_connues: dict, chansons_actuelles: dict) -> list:
    # 1. Détection des AJOUTS (Inchangé)
    nouvelles_chansons = []
    for nom_fichier, chemin in chansons_actuelles.items():
        if nom_fichier not in chansons_connues:
            nouvelles_chansons.append(chemin)
            
    if nouvelles_chansons:
        ecrire_log(NOM_MODULE, f"Reçu {len(nouvelles_chansons)} nouvelle(s) chanson(s) !")
        for chemin in nouvelles_chansons:
            ecrire_log(NOM_MODULE, f"-> Nouveau MP3 reçu : {chemin}")

    # 2. MODIFICATION : Détection des SUPPRESSIONS
    chansons_supprimees = []
    for nom_fichier, chemin in chansons_connues.items():
        if nom_fichier not in chansons_actuelles:
            chansons_supprimees.append(chemin)
            
    if chansons_supprimees:
        ecrire_log(NOM_MODULE, f"Attention : {len(chansons_supprimees)} chanson(s) ont été supprimée(s) !")
        for chemin in chansons_supprimees:
            ecrire_log(NOM_MODULE, f"-> MP3 supprimé : {chemin}")

    # 3. Si rien n'a bougé (ni ajout, ni suppression)
    if not nouvelles_chansons and not chansons_supprimees:
        ecrire_log(NOM_MODULE, "Scan de routine : Aucun changement détecté (ni ajout, ni suppression).")
        
    return nouvelles_chansons