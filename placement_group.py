import boto3

#ec2_client = boto3.client('ec2')
#sts_client = boto3.client('sts')
# Assuming the user has AccessKeyId or any access to be honest,
# we can retrieve the account details.
# 1. Get the account details.
# 2. Get regions for the connected user, c2.describe_regions()
#   and availability zones.
# 3. Iterate through the regions and describe placement groups.

#caller_identity = sts_client.get_caller_identity()
#active_regions = ec2_client.describe_regions(
#    Filters=[{
#        'Name': 'opt-in-status',
#        'Values': ['opted-in']
#    }]
#)

#active_availability_zones = ec2_client.describe_availability_zones()


# Method to create_session.
def create_session(region, profile=None):
    if profile is not None:
        return boto3.session.Session(profile_name=profile, region_name=region)
    else:
        return boto3.session.Session(region_name=region)


# Method hard-coding the accounts in the code.
def get_aws_accounts():
    return ["stlb"]


# Method for hard coding the region.
# Note to create a dict of account and regions
def get_regions_for_stlb_account():
    return ["use-east-1", "us-east-2"]


# Trial method for printing placement group
def print_placement_group(placement_group_response):
    for group in placement_group_response['PlacementGroups']:
        print(group['GroupName'])


print("Starting to get accounts ....")
aws_accounts = get_aws_accounts()

for account in aws_accounts:
    print("Processing account ", account)
    regions = get_regions_for_stlb_account()
    for region in regions:
        print("Establishing a session for account " + account + " and region " + region)
        session = create_session(region, account)
        ec2_client = session.client("ec2")
        response = ec2_client.describe_placement_groups()
        print_placement_group(response)
