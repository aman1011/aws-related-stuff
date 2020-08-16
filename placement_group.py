import boto3
from botocore.exceptions import UnknownClientMethodError, ProfileNotFound
import pandas


def create_session(region, profile=None):
    """
    Creates Active session for a profile and region combination
    :param region: AWS region
    :param profile: AWS profile
    :return: boto3 session
    """
    if profile is not None:
        return boto3.session.Session(profile_name=profile, region_name=region)
    else:
        return boto3.session.Session(region_name=region)


def get_aws_accounts():
    """
    Helper method get the hard coded AWS accounts
    :return: account-profile name
    """
    return ["stlb"]


def get_regions_for_stlb_account():
    """
    Helper method to get the hard coded regions
    :return: list of region names
    """
    return ["us-east-1", "us-east-2"]


def get_instances_for_placement_group(ec2_client, placement_group_name):
    """
    Get the list of instances for a placement group
    :param ec2_client: ec2_client
    :param placement_group_name: placement group name
    :return: list of instance id's
    """
    print("Calling describe instances API ....")
    instance_response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'placement-group-name',
                'Values': [placement_group_name]
            }
        ]
    )

    # For every reservations, iterate over and find the
    # instances Key and iterate over the value of Instances key
    # and look for key instanceId.
    instances = []
    for reservation in instance_response['Reservations']:
        instances.append([instance['InstanceId'] for instance in reservation['Instances']])

    return instances


print("Starting to get accounts ....")
aws_accounts = get_aws_accounts()
placement_group_instance_dict = {}

for account in aws_accounts:
    print("Processing account ", account)
    regions = get_regions_for_stlb_account()
    for region in regions:
        print("Establishing a session for account " + account + " and region " + region)
        session = None
        try:
            session = create_session(region, account)
        except ProfileNotFound as e:
            print(f"Session could not be established for the account profile {account} and region {region}")
            print(e)
        print("Session established ....")
        ec2_client = session.client("ec2")
        print("Calling the describe placement API ....")
        placement_group_response = ec2_client.describe_placement_groups()

        # Iterate over the placement group and use
        # it to filter the instances.
        # Create a dictionary of the data.
        print("Creating local dictionary ....")
        for group in placement_group_response['PlacementGroups']:
            try:
                placement_group_instance_dict[group['GroupName']] = get_instances_for_placement_group(ec2_client, group['GroupName'])
            except UnknownClientMethodError as e:
                print(f"Failed in getting instance info for {group['GroupName']} ....")


# Now we write the data in a file using pandas
print("Writing data to local file ....")
with open('new_data.txt', 'w') as f:
    f.write("Placement-Group Name:  \t\t\t InstanceIds \n")
    count = 1
    for key in placement_group_instance_dict.keys():
        if placement_group_instance_dict[key] == []:
            f.write(str(count) + ". " + key + ":  " + "Empty " + "\n")
            count = count + 1
        else:
            f.write(str(count) + ". " + key + ": ")
            count = count + 1
            for i in placement_group_instance_dict[key]:
                for j in i:
                    f.write(j + ", ")
            f.write("\n")


print("Done ....")
