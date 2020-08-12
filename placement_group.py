import boto3

ec2_client = boto3.client('ec2')
sts_client = boto3.client('sts')
# Assuming the user has AccessKeyId or any access to be honest,
# we can retrieve the account details.
# 1. Get the account details.
# 2. Get regions for the connected user, c2.describe_regions()
#   and availability zones.
# 3. Iterate through the regions and describe placement groups.

caller_identity = sts_client.get_caller_identity()
active_regions = ec2_client.describe_regions(
    Filters=[{
        'Name': 'opt-in-status',
        'Values': ['opted-in']
    }]
)

active_availability_zones = ec2_client.describe_availability_zones()

response = ec2_client.describe_placement_groups()
for group in response['PlacementGroups']:
    print(group['GroupName'])
