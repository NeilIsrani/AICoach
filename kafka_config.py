from confluent_kafka import Producer, Consumer
import json

KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
LEADERBOARD_TOPIC = 'weekly_leaderboard'
PREDICTION_TOPIC = 'strain_predictions'

def get_producer():
    return Producer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'client.id': 'healthbud-producer'
    })

def get_consumer():
    return Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'healthbud-consumer',
        'auto.offset.reset': 'earliest'
    }) 