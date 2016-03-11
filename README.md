# Add EC2 metadata as global variable to syslog-ng config

This is a super simple script and an SCL file which can be include in syslog-ng.conf after the ec2metadata.py file is copied to /etc/syslog-ng/ directory. The python file needs the "boto3" and "requests" libraries. The python script generaties a series of @define pragmas for the global variables, all of the variables are prefixed with the "aws." prefix. Valid variables are: 
 * Architecture
 * AmiLaunchIndex
 * ClientToken
 * EbsOptimized
 * Hypervisor
 * ImageId
 * InstanceId
 * InstanceType
 * KeyName
 * PrivateDnsName
 * PrivateIpAddress
 * PublicDnsName
 * PublicIpAddress
 * RootDeviceName
 * RootDeviceType
 * SubnetId
All of the tags are also added as global variables. The tag name syntax is the following: aws.Tag.<tag_name>

If this script runs on a non-EC2 machine, the output will be empty.
