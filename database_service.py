import pandas as pd
from rabbitmq_utils import connection
from pika.exceptions import ChannelClosed 
import sys
import json
from datetime import datetime


def userdataqueue_callback(ch, method, properties, body):
    
    try:
        data = json.loads(body)
        
        #convert date column to datetime type
        df = pd.read_csv('./database/transactions.csv', names=['email', 'date', 'amount'])
        # df.iloc[:, 1] = pd.to_datetime(df.iloc[:, 1], format="%Y-%m-%d",).dt.date
        df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d").dt.date

        user_email = data['email']     #str.strip(str.lower(data['email']))
        date_from = datetime.strptime(data['date_from'], "%Y-%m-%d").date()
        date_to =  datetime.strptime(data['date_to'], "%Y-%m-%d").date()

        
        filtered_data = df[(df['date'] > date_from) & (df['date'] < date_to) & (df['email'] == user_email)]
        dates = filtered_data.date.map(lambda x: x.strftime("%Y-%m-%d"))
        transactions = {"email": user_email, "transactions" :dict(zip(dates, filtered_data.amount))}
        
        channel.exchange_declare(exchange='transactions', exchange_type='direct', durable=True)
        channel.queue_declare(queue='transactions.queue')
        channel.queue_bind(exchange='transactions', queue='transactions.queue', routing_key='transactions.queue')
        
        transactions = json.dumps(transactions)
        channel.basic_publish(exchange='transactions', routing_key='transactions.queue', body= transactions)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print('Published to transactions queue')
    
    except Exception as e:
        print(str(e))
        sys.exit()
        



channel = None

try:
        
    channel = connection()
    channel.queue_declare(queue='user_data.queue')
    
    channel.basic_consume(queue='user_data.queue', on_message_callback=userdataqueue_callback) #, auto_ack=True)
    channel.start_consuming()
    print('Waiting for messages')
    
    
except ChannelClosed as e:
    print(str(e))
    
except KeyboardInterrupt:
    print('Database service exited')
    sys.exit()
