from socket import timeout

#pip install kavenegar
from kavenegar import *
try:
    api = KavenegarAPI('6D756C62446F683446515A315A6E484B69426E4A4F4F6350527253594A35464C426F76485858784D52586B3D')
    params = {
        'sender': '10008663',#optional
        'receptor': '09357108164',#multiple mobile number, split by comma
        'message': 'سلام عشقم چطوری!!!!!',
    } 
    response = api.sms_send(params)
    print(response)
except APIException as e: 
    print(e)
except HTTPException as e: 
    print(e)