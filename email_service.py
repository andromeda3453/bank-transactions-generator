from rabbitmq_utils import connection
from pika.exceptions import ChannelClosed 
import sys, os, json, smtplib, ssl
from minio import Minio
import config
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

channel = None

def pdfqueue_callback(ch, method, properties, body):
    
    try:
        data = json.loads(body)
        
        #download file to email
        client = Minio(
            "play.min.io",
            access_key="Q3AM3UQ867SPQQA43P2F",
            secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
        )

        if (not os.path.exists("transaction_pdfs_to_upload")):
            os.mkdir('transaction_pdfs_to_upload')

        file_path = f'transaction_pdfs_to_email/{data["file_name"]}'
        
        client.fget_object('transactionpdfs', data['file_name'], file_path)
        
        #email file
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.connect("smtp.gmail.com",587)
        server.starttls(context=context)
        server.login(config.EMAIL, config.PASSWORD)
        
        message = MIMEMultipart()
        message['To'] = data['email']
        message['From'] = config.EMAIL
        message['Subject'] = 'Your transaction history'
        
        with open(file_path, 'rb') as file: 
            attachment = MIMEApplication(file.read(),_subtype="pdf")
            
        attachment.add_header('Content-Disposition','attachment',filename=str(data["file_name"]))
        message.attach(attachment)
        
        server.send_message(message)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
        #delete file after email sent
        if os.path.exists(file_path):
            os.remove(file_path)
        
        print('Email Sent')
    except Exception as e:
        print(str(e))
        sys.exit()
        





try:
        
    channel = connection()
    channel.queue_declare(queue='pdf.queue')
    
    channel.basic_consume(queue='pdf.queue', on_message_callback=pdfqueue_callback)
    channel.start_consuming()
    print('Waiting for messages')
    
    
except ChannelClosed as e:
    print(str(e))
    
except KeyboardInterrupt:
    print('Email service exited')
    sys.exit()