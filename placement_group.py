import boto3

ec2_client = boto3.client('ec2')
response = ec2_client.describe_placement_groups()

for group in response['PlacementGroups']:
    print(group['GroupName'])
