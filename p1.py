import os
import pika
from logs import ecrire_log
import time

NOM_MODULE = "P1"
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'file_chansons'

DOSSIER_A_ECOUTER = "./repertoire"
TEMPS_ATTENTE = 10  # 5 minutes

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

def envoyer_a_rabbitmq(chemin_mp3: str):
    """Envoie le chemin du MP3 dans la queue RabbitMQ."""
    try:
        # Connexion au serveur RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        
        # Déclaration de la file (si elle n'existe pas, elle est créée)
        channel.queue_declare(queue=QUEUE_NAME)
        
        # Publication du message
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=chemin_mp3
        )
        ecrire_log(NOM_MODULE, f"Message envoyé à RabbitMQ -> {chemin_mp3}")
        connection.close()
    except Exception as e:
        ecrire_log(NOM_MODULE, f"Erreur de connexion RabbitMQ : {e}")

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
            envoyer_a_rabbitmq(chemin)

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


def main():

    ecrire_log(NOM_MODULE, "Démarrage du programme P1.")

    chansons_connues = recuperer_mp3(DOSSIER_A_ECOUTER)

    while True:
        try:
            time.sleep(TEMPS_ATTENTE)

            chansons_actuelles = recuperer_mp3(DOSSIER_A_ECOUTER)

            verifier_nouvelles_chansons(
                chansons_connues,
                chansons_actuelles
            )

            chansons_connues = chansons_actuelles

        except KeyboardInterrupt:
            ecrire_log(NOM_MODULE, "Arrêt de P1.")
            break

if __name__ == "__main__":
    main()