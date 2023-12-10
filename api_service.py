from fastapi import FastAPI
from pydantic import BaseModel
from rabbitmq_utils import connection
# import pika
import sys, re

channel = None
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

class ClientInfo(BaseModel):
    
    email: str
    date_from: str
    date_to: str

try:
    
    channel = connection()
    channel.exchange_declare(exchange='user_data', exchange_type='direct', durable=True)
    channel.queue_declare(queue='user_data.queue')
    channel.queue_bind(exchange='user_data', queue='user_data.queue', routing_key='user_data.queue' )
    
    app = FastAPI()
except:
    print('Unable to establish connection to RabbitMQ server. Please make sure it is running and try again.')
    sys.exit()

@app.post("/pdf")
def generate_pdf(info: ClientInfo):
    try:
        
        if (re.fullmatch(EMAIL_REGEX, info.email)):
        
            if channel:
                message = f'{{"email": "{info.email}", "date_from": "{info.date_from}", "date_to": "{info.date_to}"}}'
                print(message)
                channel.basic_publish(exchange='user_data', routing_key='user_data.queue', body= message)
                print('Published to userdata queue')
                return {"message": 'request recieved. Please check your email.'}
            else: 
                return {"error": "RabbitMQ server not running"}
        else:
            return {"error": 'Invalid Email'}
        
    except Exception as e:
        return str(e)



