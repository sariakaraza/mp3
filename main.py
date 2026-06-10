# main.py
import time
from logs import ecrire_log
from p1 import recuperer_mp3, verifier_nouvelles_chansons

DOSSIER_A_ECOUTER = "./repertoire"
TEMPS_ATTENTE = 10 

def main():
    # Log tagué avec "MAIN"
    ecrire_log("MAIN", "Démarrage de l'application via main.py.")
    print(f"Surveillance du dossier '{DOSSIER_A_ECOUTER}' activée...")
    
    chansons_connues = recuperer_mp3(DOSSIER_A_ECOUTER)
    
    nb_existantes = len(chansons_connues)
    # Log tagué avec "MAIN"
    ecrire_log("MAIN", f"Initialisation : {nb_existantes} chanson(s) déjà présente(s).")
    
    if nb_existantes > 0:
        for nom_fichier, chemin in chansons_connues.items():
            ecrire_log("MAIN", f"-> Chanson existante : {chemin}")
    
    while True:
        try:
            time.sleep(TEMPS_ATTENTE)
            
            chansons_actuelles = recuperer_mp3(DOSSIER_A_ECOUTER)
            nouvelles = verifier_nouvelles_chansons(chansons_connues, chansons_actuelles)
            
            if nouvelles:
                print(f"[{time.strftime('%H:%M:%S')}] {len(nouvelles)} nouveau(x) MP3 détecté(s).")
            
            chansons_connues = chansons_actuelles
            
        except KeyboardInterrupt:
            ecrire_log("MAIN", "Arrêt de l'application (Ctrl+C).")
            print("\nProgramme arrêté avec succès.")
            break

if __name__ == "__main__":
    main()