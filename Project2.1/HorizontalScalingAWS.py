import re

import boto3
import time
import requests

# EC2 Variables
INSTANCE_TYPE = "m3.medium"
LOAD_GENERATOR = "ami-6b987a11"
WEB_SERVICE = "ami-b7987acd"
REGION = 'us-east-1'

# Class Variable
PASSWORD = "KX498wCcMHqy7EvjVYkKGR"
ANDREW_ID = "fy2"
KEY = "PROJECT"
VALUE = "2.1"

# Connect to EC2
ec2 = boto3.resource('ec2', region_name=REGION)
client = boto3.client('ec2', region_name=REGION)

total_instance = 1

def create_instance(image):
    instance = ec2.create_instances(ImageId=image, InstanceType='t2.micro',
                                    MaxCount=1,
                                    MinCount=1,
                                    TagSpecifications=[
                                        {
                                            'ResourceType': 'instance',
                                            'Tags': [
                                                {
                                                    'Key': KEY,
                                                    'Value': VALUE
                                                }]
                                        }
                                    ],
                                    SecurityGroups=['project2'])

    instance[0].wait_until_running()
    print('Create instance successfully')
    instance[0].reload()
    DNS_instance = instance[0].public_dns_name
    print('Instance DNS is : ' + DNS_instance)
    return DNS_instance


def get_rps(log):
    minute = re.findall('[0-9]+', log.split('Minute')[-1].strip())[0]
    rps = log.split('rps=')[-1].replace(']', '')
    return int(minute), float(rps)


# DNS_LG = create_instance(LOAD_GENERATOR)
# DNS_WS = create_instance(WEB_SERVICE)

DNS_LG = 'ec2-34-227-61-90.compute-1.amazonaws.com'
DNS_WS = 'ec2-54-157-248-96.compute-1.amazonaws.com'

# userInfo = {'passwd': PASSWORD, 'andrewid': ANDREW_ID}
# authenticate = 'http://' + DNS_LG + '/password'
# auth_request = requests.get(authenticate, params=userInfo)
# print("Successfully authenticate with the load generator!")
#
# wsInfo = {'dns': DNS_WS}
# submit = 'http://' + DNS_LG + '/test/horizontal'
# submit_request = requests.get(submit, params=wsInfo)
# print("Successfully submit the web service VM's DNS name to the load generator to start the test!")
#
# idx_begin = submit_request.text.find('log?name')
# idx_end = submit_request.text.find("\'>Test")
# testLog = submit_request.text[idx_begin: idx_end]

testLog = 'log?name=test.1505882858216.log'
monitor = 'http://' + DNS_LG + '/' + testLog
monitor_request = requests.get(monitor)
print(monitor_request.text)

while 'Minute' not in monitor_request.text:
    time.sleep(1000)
    monitor_request = requests.get(monitor)

minute, rps = get_rps(monitor_request.text)

while rps <= 4000:
    start_time = time.time()
    print('Current RPS is : ' + str(rps))
    DNS_WS_ADD = create_instance(WEB_SERVICE)

    add_info = {'dns': DNS_WS_ADD}
    add = 'http://' + DNS_LG + '/test/horizontal/add'

    add_request = requests.get(add, params=add_info)

    while 'added' not in add_request.text:
        add_request = requests.get(add, params=add_info)

    total_instance += 1
    print('Successfully add a instance! Current instance number is ' + str(total_instance))
    end_time = time.time()

    if end_time - start_time < 100:
        time.sleep(100 - (end_time - start_time))

    monitor_request = requests.get(monitor)
    cur_minute, rps = get_rps(monitor_request.text)

    while cur_minute == minute:
        cur_minute, rps = get_rps(monitor_request.text)

print('Test finished! The test id is ' + re.findall('[0-9]+', testLog)[0])



