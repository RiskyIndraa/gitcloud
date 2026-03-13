import boto3
import uuid
import json
from datetime import datetime

# Inisialisasi resource di luar handler agar bisa di-reuse oleh AWS (best practice)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('LKS-UserLogs')

def lambda_handler(event, context):
    try:
        user_email = 'unknown'
        
        # 1. Parsing jika event berasal dari output API Gateway (berupa string JSON di dalam "body")
        if 'body' in event:
            try:
                body_data = json.loads(event['body'])
                user_email = body_data.get('email', 'unknown')
            except Exception:
                pass
        # 2. Parsing jika event merupakan payload dictionary langsung
        elif isinstance(event, dict):
            user_email = event.get('email', 'unknown')

        # Menyimpan log aktivitas ke DynamoDB
        response = table.put_item(
            Item={
                'log_id': str(uuid.uuid4()),
                'timestamp': datetime.utcnow().isoformat(),
                'activity': 'USER_REGISTRATION',
                'details': f'Pendaftaran user dengan email: {user_email}'
            }
        )
        
        # Mengembalikan event aslinya dengan tambahan status log agar Step Functions selanjutnya berjalan mulus
        event['log_status'] = 'DynamoDB_Success'
        return event

    except Exception as e:
        print(f"Error pada DynamoDB Logger: {e}")
        # Lemparkan kembali errornya agar ditangkap oleh fitur 'Catch' di Step Functions
        raise e
