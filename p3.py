import pika
import json
from logs import ecrire_log

NOM_MODULE = "P3"

RABBITMQ_HOST = "localhost"
QUEUE_METADATA = "file_metadata"


def traiter_metadata(metadata):

    ecrire_log(
        NOM_MODULE,
        f"Metadata reçue : "
        f"Titre={metadata['titre']}, "
        f"Artiste={metadata['artiste']}, "
        f"Album={metadata['album']}, "
        f"Duree={metadata['duree']}s"
    )

    print("\n===== METADATA RECUE =====")

    print("Chemin :", metadata["chemin"])
    print("Titre :", metadata["titre"])
    print("Artiste :", metadata["artiste"])
    print("Album :", metadata["album"])
    print("Durée :", metadata["duree"])

    print("==========================\n")


def callback(ch, method, properties, body):

    try:

        metadata = json.loads(
            body.decode()
        )

        traiter_metadata(
            metadata
        )

    except Exception as e:

        ecrire_log(
            NOM_MODULE,
            f"Erreur traitement : {e}"
        )


def main():

    ecrire_log(
        NOM_MODULE,
        "Démarrage du programme P3."
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST
        )
    )

    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_METADATA
    )

    ecrire_log(
        NOM_MODULE,
        "En attente des metadata..."
    )

    channel.basic_consume(
        queue=QUEUE_METADATA,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()


if __name__ == "__main__":
    main()