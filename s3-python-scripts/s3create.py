import boto3
import botocore.exceptions
import random
import string

s3_client = boto3.client('s3')

# Define a base name for the S3 bucket
base_name = 's3-for-data-backup'

# Function to generate a unique bucket name
def generate_unique_bucket_name(base_name):
    random_suffix = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    return f"{base_name}-{random_suffix}"

# Attempt to create an S3 bucket with a unique name
try:
    # Generate a unique bucket name
    unique_bucket_name = generate_unique_bucket_name(base_name)

    # Create the S3 bucket
    response = s3_client.create_bucket(
        Bucket=unique_bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-south-2'
        }
    )

    # Print the response
    print(f"Bucket '{unique_bucket_name}' created successfully.")

    # Enable versioning for the bucket
    s3_client.put_bucket_versioning(
        Bucket=unique_bucket_name,
        VersioningConfiguration={
            'Status': 'Enabled'
        }
    )
    print(f"Versioning enabled for '{unique_bucket_name}'.")

except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'BucketAlreadyExists':
        # Handle the case where the bucket name is not unique
        print(f"Bucket name '{unique_bucket_name}' is not unique. Generating a new name...")
        unique_bucket_name = generate_unique_bucket_name(base_name)
        response = s3_client.create_bucket(
            Bucket=unique_bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-south-2'
            }
        )
        print(f"New bucket '{unique_bucket_name}' created.")

        # Enable versioning for the new bucket
        s3_client.put_bucket_versioning(
            Bucket=unique_bucket_name,
            VersioningConfiguration={
                'Status': 'Enabled'
            }
        )
        print(f"Versioning enabled for '{unique_bucket_name}'.")

    else:
        # Handle other exceptions
        print(f"An error occurred: {e}")

# Use this code after creating the S3 bucket to wait until it is available and ready for use.
waiter = s3_client.get_waiter('bucket_exists')
waiter.wait(
    Bucket=unique_bucket_name,
    ExpectedBucketOwner='816827255260',  # Replace with your expected owner ID
    WaiterConfig={
        'Delay': 5,
        'MaxAttempts': 12
    }
)

print(response)
