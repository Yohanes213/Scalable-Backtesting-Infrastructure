from kafka import KafkaAdminClient
from kafka.admin import NewTopic
import json
from kafka import KafkaProducer

# Define Kafka connection parameters
#bootstrap_servers = 'kafka:9092' 

# # Create admin client
# admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

# # Define topics to create
# topics = ['backend_requests', 'backtest_results']

# # Check if topics exist, create them if not
# existing_topics = admin_client.list_topics()
# for topic in topics:
#     if topic not in existing_topics:
#         new_topic = NewTopic(name=topic, num_partitions=1, replication_factor=1)
#         admin_client.create_topics(new_topics=[new_topic])

# # Close admin client
# admin_client.close()

# Create Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_backend_request(name, start_date, end_date, strategy, params, start_cash, comm):
    message = {
        'name': name,
        'start_date': start_date,
        'end_date': end_date,
        'strategy': strategy,
        'params': params,
        'start_cash': start_cash,
        'comm': comm
    }

    # Produce message to backend_requests topic
    producer.send('backend_requests', value=message)
    producer.flush()

# Define function to send backtest results
def send_backtest_results(metrics):
    message = {
        'metrics': metrics
    }
    producer.send('backtest_results', value=message)
    producer.flush()
