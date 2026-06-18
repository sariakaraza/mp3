import pika
import json
import threading
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from logs import ecrire_log


NOM_MODULE = "P3"

RABBITMQ_HOST = "localhost"
QUEUE_METADATA = "file_metadata"

app = Flask(__name__)
CORS(app)

metadata_stockees = []


def callback(ch, method, properties, body):

    try:

        metadata = json.loads(
            body.decode()
        )

        metadata_stockees.append(
            metadata
        )

        ecrire_log(
            NOM_MODULE,
            f"Metadata reçue : {metadata['titre']}"
        )

    except Exception as e:

        ecrire_log(
            NOM_MODULE,
            f"Erreur RabbitMQ : {e}"
        )


def ecouter_rabbit():

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
        "RabbitMQ en écoute"
    )

    channel.start_consuming()


@app.get("/api/mp3")
def get_mp3():

    return jsonify(
        metadata_stockees
    )


@app.post("/api/mp3/confirm")
def confirmer():

    body = request.get_json()

    chemin = body["chemin"]

    try:

        if os.path.exists(
            chemin
        ):

            os.remove(
                chemin
            )

            global metadata_stockees

            metadata_stockees = [
                m
                for m in metadata_stockees
                if m["chemin"] != chemin
            ]

            ecrire_log(
                NOM_MODULE,
                f"Fichier supprimé : {chemin}"
            )

            return {
                "success": True
            }

        return {
            "success": False
        }

    except Exception as e:

        ecrire_log(
            NOM_MODULE,
            str(e)
        )

        return {
            "success": False
        }, 500


def main():

    thread = threading.Thread(
        target=ecouter_rabbit,
        daemon=True
    )

    thread.start()

    app.run(
        port=5000,
        debug=True
    )


if __name__ == "__main__":
    main()