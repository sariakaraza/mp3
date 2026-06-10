import pika
from mutagen import File
from logs import ecrire_log

NOM_MODULE = "P2"
RABBITMQ_HOST = "localhost"
QUEUE_NAME = "file_chansons"

def extraire_metadata(chemin_mp3):
    try:
        audio = File(chemin_mp3, easy=True)

        if audio is None:
            ecrire_log(
                NOM_MODULE,
                f"Impossible de lire le fichier : {chemin_mp3}"
            )
            return

        duree = round(audio.info.length)

        metadata = {
            "titre": audio.get("title", ["Inconnu"])[0],
            "artiste": audio.get("artist", ["Inconnu"])[0],
            "album": audio.get("album", ["Inconnu"])[0],
            "duree": duree
        }

        ecrire_log(
            NOM_MODULE,
            f"Metadata extraite : "
            f"Titre={metadata['titre']}, "
            f"Artiste={metadata['artiste']}, "
            f"Album={metadata['album']}, "
            f"Duree={metadata['duree']}s"
        )

    except Exception as e:
        ecrire_log(
            NOM_MODULE,
            f"Erreur extraction metadata : {e}"
        )

def callback(ch, method, properties, body):

    chemin_mp3 = body.decode()

    ecrire_log(
        NOM_MODULE,
        f"Message reçu depuis RabbitMQ : {chemin_mp3}"
    )

    extraire_metadata(chemin_mp3)

def main():

    ecrire_log(
        NOM_MODULE,
        "Démarrage du consommateur RabbitMQ."
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )

    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)

    ecrire_log(
        NOM_MODULE,
        f"En attente de messages sur la file '{QUEUE_NAME}'."
    )

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()

if __name__ == "__main__":
    main()