import pika
import json
import time

from logs import ecrire_log

NOM_MODULE = "P3"

RABBITMQ_HOST = "localhost"
QUEUE_METADATA = "file_metadata"


def envoyer_api(metadata):

    ecrire_log(
        NOM_MODULE,
        "Début appel API (simulation)"
    )

    time.sleep(2)

    print("\n===== DONNEES ENVOYEES =====")

    print(json.dumps(
        metadata,
        indent=4,
        ensure_ascii=False
    ))

    print("===========================\n")

    ecrire_log(
        NOM_MODULE,
        "API simulée : succès"
    )

    return True


def traiter_metadata(metadata):

    ecrire_log(
        NOM_MODULE,
        f"Metadata reçue : {metadata['titre']}"
    )

    succes = envoyer_api(
        metadata
    )

    if succes:

        ecrire_log(
            NOM_MODULE,
            "Traitement terminé."
        )


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
            f"Erreur : {e}"
        )


def main():

    ecrire_log(
        NOM_MODULE,
        "Démarrage P3."
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

    channel.basic_consume(
        queue=QUEUE_METADATA,
        on_message_callback=callback,
        auto_ack=True
    )

    ecrire_log(
        NOM_MODULE,
        "En attente des metadata..."
    )

    channel.start_consuming()


if __name__ == "__main__":
    main()