
from kafka_queue import KafkaQueue

class QueueDAO:
    def __init__(self, type):
        if type in ['kafka']:
            self.queue = KafkaQueue.get_queue_connection()
            
    def send_message(self, topic, data):
        self.queue.send(topic, data)
    
    def recieve_message(self, topic):
        return self.queue.recieve(topic)
    
    def recieve_stream(self, topic):
        return self.queue.recieve_stream(topic)

        