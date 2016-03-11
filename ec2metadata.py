#!/usr/bin/python
import boto3
import pprint
import requests
import sys

instance_keys = ['Architecture', 'AmiLaunchIndex', 'ClientToken', 'EbsOptimized', 'Hypervisor', 'ImageId', 'InstanceId', 'InstanceType', 'KeyName', 'PrivateDnsName',
                 'PrivateIpAddress', 'PublicDnsName', 'PublicIpAddress', 'RootDeviceName', 'RootDeviceType', 'SubnetId']


def get_instance_metadata():
    data = requests.get(
        "http://169.254.169.254/latest/dynamic/instance-identity/document", timeout=2)
    instance_id = data.json()['instanceId']
    account_id = data.json()['accountId']
    region = data.json()['region']
    return (instance_id, account_id, region)


def get_aws_instance_information(region, instance_id, account_id):
    ec2 = boto3.client("ec2", region)
    res = ec2.describe_instances(InstanceIds=[instance_id])
    instance = res['Reservations'][0]['Instances'][0]
    env = [tag['Value']
           for tag in instance['Tags'] if tag['Key'] == 'Environment'][0]
    res = {}
    for key in instance_keys:
        res[key] = instance[key]
    for tag in instance['Tags']:
        res['Tag.{0}'.format(tag['Key'].replace(":", "_"))] = tag['Value']
    res['AccountId'] = account_id
    return res

try:
    (instance_id, account_id, region) = get_instance_metadata()
except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
    sys.exit(0)

res = get_aws_instance_information(region, instance_id, account_id)
for key, value in res.iteritems():
    print "@define aws.{0} \"{1}\"".format(key, value)
