#!/usr/bin/env python

import json
import os
import pprint
import time
import uuid

import boto.ec2

# boto will look for AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env vars.
KEY_NAME = os.environ['KEY_NAME']
TAG_NAME = os.environ['TAG_NAME']
DOCKER_ENV = json.loads(os.environ['DOCKER_ENV'])

startup_script = '''#!/bin/sh
set -e
sudo apt-get update
sudo apt-get install -y docker.io
'''

context = {
    'image': 'fordhurley/eb-docker-test:' + TAG_NAME,
    'cmd': 'nodejs worker.js',
    'env': ' '.join('-e {k}={v}'.format(k=k, v=v) for k, v in DOCKER_ENV.iteritems()),
}
run_command = 'sudo docker.io run -d {env} {image} {cmd}'.format(**context)
startup_script += '\n' + run_command + '\n'

conn = boto.ec2.connect_to_region('us-east-1')

print 'Requesting block device'
dev_sda1 = boto.ec2.blockdevicemapping.BlockDeviceType(delete_on_termination=True)
dev_sda1.size = 8 # GB
bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
bdm['/dev/sda1'] = dev_sda1

print 'Requesting instance'
res = conn.run_instances('ami-84562dec',
                         key_name=KEY_NAME,
                         instance_type='t1.micro',
                         security_groups=['ssh'],
                         block_device_map=bdm,
                         user_data=startup_script)

print '->', res

instance = res.instances[0]

print '->', instance

print 'Waiting for instance to start'
status = 'pending'
while status == 'pending':
    time.sleep(1)
    status = instance.update()
print status

worker_type = 'eb-docker-test-worker'
tags = {
    'Name': worker_type + '-' + str(uuid.uuid4()),
    'WorkerType': worker_type
}
print 'Adding tags:'
pprint.pprint(tags)
instance.add_tags(tags)

print '->', instance.public_dns_name
