from rabbitmq_utils import connection
from pika.exceptions import ChannelClosed 
import sys, os, json, random
from fpdf import FPDF
from minio import Minio



channel = None

def transactionsqueue_callback(ch, method, properties, body):
    
    # pdf dims  = 210 x 297
    try:
        data = json.loads(body)
        print(data['transactions'])
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40, 10, data['email'], ln= 1)
        pdf.ln()
        pdf.set_font('Arial', "", 12)
        
        if len(data['transactions']) > 0:
            for key, value in data['transactions'].items():
                
                pdf.cell(w=10, h=10, txt=f'{key} ------> {str(value)}')
                pdf.ln()
        else:
            pdf.cell(w=10, h=10, txt='No transactions')
            
        
        
        pdf_name = f'transac{random.randint(1,100000)}.pdf'
        pdf.output(name=f'transaction_pdfs_to_upload/{pdf_name}', dest='F')
        
        
        #upload pdf to object storage
        client = Minio(
            "play.min.io",
            access_key="Q3AM3UQ867SPQQA43P2F",
            secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
        )
        
        bucket_exists = client.bucket_exists("transactionpdfs")
        
        if not bucket_exists:
            client.make_bucket("transactionpdfs")
        else:
            print("Bucket 'transactionpdfs' already exists")
            
        if (not os.path.exists("transaction_pdfs_to_upload")):
            os.mkdir('transaction_pdfs_to_upload')
        
        result = client.fput_object('transactionpdfs', pdf_name, f'transaction_pdfs_to_upload/{pdf_name}')
        print(f'Uploaded {pdf_name}')
        
        # client.fget_object('transactionpdfs', pdf_name, f'transaction_pdfs_to_email/{pdf_name}')
        
        payload = {"email": data['email'], "file_name": pdf_name}
        payload = json.dumps(payload)
        #publish file name for email service
        channel.exchange_declare(exchange='pdf', exchange_type='direct', durable=True)
        channel.queue_declare(queue='pdf.queue')
        channel.queue_bind(exchange='pdf', queue='pdf.queue', routing_key='pdf.queue')
        
        channel.basic_publish(exchange='pdf', routing_key='pdf.queue', body= payload)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        #delete file after publish
        if os.path.exists(f'transaction_pdfs_to_upload/{pdf_name}'):
            os.remove(f'transaction_pdfs_to_upload/{pdf_name}')
            
        print('Published to pdf queue')
    except Exception as e: 
        print(str(e))
        sys.exit()
    

    



try:
        
    channel = connection()
    channel.queue_declare(queue='transactions.queue')
    
    channel.basic_consume(queue='transactions.queue', on_message_callback=transactionsqueue_callback)
    channel.start_consuming()
    print('Waiting for messages')
    
    
except ChannelClosed as e:
    print(str(e))
    
except KeyboardInterrupt:
    print('PDF service exited')
    sys.exit()