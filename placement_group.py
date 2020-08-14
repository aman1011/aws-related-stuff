import boto3
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
    instance_response = ec2_client.describe_instnaces(
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
        session = create_session(region, account)
        print(session)
        ec2_client = session.client("ec2")
        placement_group_response = ec2_client.describe_placement_groups()
        print_placement_group(placement_group_response)

        # Iterate over the placement group and use
        # it to filter the instances.
        # Create a dictionary of the data.
        for group in placement_group_response['PlacementGroups']:
            placement_group_instance_dict[group['GroupName']] = get_instances_for_placement_group(ec2_client, group['GroupName'])


# Now we write the data in a file using pandas
with open('new_data.txt', 'w') as f:
    for key in placement_group_instance_dict.keys():
        if placement_group_instance_dict[key] == []:
            f.write(key + ":  " + "Empty " + "\n")
        else:
            f.write(key + ": ")
            for i in placement_group_instance_dict[key]:
                for j in i:
                    f.write(j + " " + "\n")
