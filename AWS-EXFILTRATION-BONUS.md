# Potential Data Exfiltration Activity in an AWS Account

This report describes three ways an attacker with valid AWS credentials could
exfiltrate data from an AWS account. The credentials may belong to a compromised
IAM user or assumed role. Although AWS considers the requests authenticated, the
activity is still unauthorized from the account owner's perspective.

## Method 1: Share an EBS snapshot with an external AWS account

1. **Description:**

   An attacker changes the permissions of an existing EBS snapshot so that an AWS
   account controlled by the attacker can use it. The external account can then
   copy the snapshot or create an EBS volume from it.

2. **Action:**

   `ec2:ModifySnapshotAttribute`

3. **Parameters:**

   - `SnapshotId`: The snapshot containing the data.
   - `Attribute`: `createVolumePermission`.
   - `OperationType`: `add`.
   - `UserId`: The external AWS account ID receiving access.
   - `Group`: If set to `all`, the snapshot becomes publicly accessible.

   An example of the relevant CloudTrail request parameters would be:

   ```json
   {
     "snapshotId": "snap-0123456789abcdef0",
     "createVolumePermission": {
       "add": {
         "items": [
           {
             "userId": "111122223333"
           }
         ]
       }
     }
   }
   ```

4. **Why do you think it is related to Exfiltration:**

   The attacker is granting an external account access to a copy of the victim's
   disk data. After receiving permission, the external account can copy the
   snapshot or create a volume and inspect its files.

   This can be difficult to notice because the original snapshot is not deleted
   or modified. From the victim account's perspective, the data still appears to
   be in its normal location.

5. **(Bonus) How to detect:**

   Monitor CloudTrail for `ModifySnapshotAttribute` events where
   `createVolumePermission` adds an account ID that is not part of the
   organization.

   Important indicators include:

   - `eventSource` is `ec2.amazonaws.com`.
   - `eventName` is `ModifySnapshotAttribute`.
   - `requestParameters.createVolumePermission.add` is present.
   - The added `userId` is not an approved AWS account.
   - The added group is `all`.
   - The request comes from an unusual source IP, region, role, or user agent.
   - The event is followed by `SharedSnapshotCopyInitiated` or
     `SharedSnapshotVolumeCreated`.

   The account can also enable EBS Block Public Access to prevent snapshots from
   being shared publicly.

## Method 2: Download objects directly from Amazon S3

1. **Description:**

   An attacker uses compromised credentials that have permission to read S3
   objects. The attacker retrieves sensitive files directly from one or more
   buckets.

2. **Action:**

   `s3:GetObject`

   If the bucket uses versioning, the attacker may also use
   `s3:GetObjectVersion` to retrieve an older version of an object.

3. **Parameters:**

   - `Bucket`: The bucket containing the information.
   - `Key`: The full name or path of the object.
   - `VersionId`: An optional identifier used to retrieve a specific object
     version.
   - `Range`: An optional value used to retrieve part of a large object.

   The relevant CloudTrail fields may look similar to:

   ```json
   {
     "eventSource": "s3.amazonaws.com",
     "eventName": "GetObject",
     "requestParameters": {
       "bucketName": "company-sensitive-data",
       "key": "customers/customer-export.csv"
     }
   }
   ```

4. **Why do you think it is related to Exfiltration:**

   `GetObject` returns the contents of the requested file to the caller. If a
   compromised identity downloads confidential files, the data crosses the
   organization's intended security boundary even though AWS considers the
   credentials valid.

   Unlike the EBS method, the attacker does not have to modify a resource policy.
   Existing read permissions may be enough to transfer the information
   immediately.

5. **(Bonus) How to detect:**

   Enable CloudTrail S3 read data events for important buckets. `GetObject` is an
   object-level data event and is not recorded by CloudTrail trails by default.

   Potential detection indicators include:

   - A sudden increase in `GetObject` requests.
   - One identity downloading many objects in a short period.
   - Access to sensitive prefixes such as `customers/`, `backups/`, `exports/`,
     or `finance/`.
   - Requests from a new IP address, country, ASN, or user agent.
   - Downloads occurring outside the identity's normal working hours.
   - One identity reading data from several unrelated buckets.
   - `GetObjectVersion` calls against old or deleted-sensitive information.
   - Object enumeration followed by a large number of downloads.

   CloudTrail data events identify the caller and requested objects. S3 server
   access logs, proxy logs, or other network telemetry can provide additional
   information about transfer volume.

## Method 3: Export a DynamoDB table to an external S3 bucket

1. **Description:**

   An attacker uses DynamoDB's point-in-time export feature to export a table into
   an S3 bucket owned by an external AWS account.

   The request must be made using credentials from the account that owns the
   table. However, the destination bucket can belong to another account if its
   policy permits the export.

2. **Action:**

   `dynamodb:ExportTableToPointInTime`

3. **Parameters:**

   - `TableArn`: The DynamoDB table being exported.
   - `S3Bucket`: The destination bucket.
   - `S3BucketOwner`: The AWS account ID that owns the destination bucket.
   - `S3Prefix`: The destination path inside the bucket.
   - `ExportTime`: The historical point from which the table is exported.
   - `ExportType`: `FULL_EXPORT` or `INCREMENTAL_EXPORT`.
   - `ExportFormat`: `DYNAMODB_JSON` or `ION`.
   - `S3SseAlgorithm`: The encryption method used for the exported files.

   An example of the important request parameters would be:

   ```json
   {
     "tableArn": "arn:aws:dynamodb:us-east-1:123456789012:table/Customers",
     "s3Bucket": "external-table-exports",
     "s3BucketOwner": "111122223333",
     "s3Prefix": "exports/customers",
     "exportType": "FULL_EXPORT",
     "exportFormat": "DYNAMODB_JSON"
   }
   ```

4. **Why do you think it is related to Exfiltration:**

   This operation transfers a copy of the DynamoDB table into an S3 bucket
   outside the victim's account. The `S3BucketOwner` parameter can identify the
   external account receiving the data.

   This method is useful to an attacker because DynamoDB performs the bulk
   transfer. The attacker does not need to generate a large number of individual
   `GetItem` or `Scan` requests.

5. **(Bonus) How to detect:**

   Monitor CloudTrail for the following activity:

   ```text
   eventSource = dynamodb.amazonaws.com
   eventName   = ExportTableToPointInTime
   ```

   Potential detection indicators include:

   - `requestParameters.s3BucketOwner` is not an account belonging to the
     organization.
   - The destination bucket is not on an approved backup or analytics bucket
     list.
   - A production or sensitive table is exported unexpectedly.
   - `exportType` is `FULL_EXPORT`.
   - The requesting identity does not normally perform database exports.
   - Point-in-time recovery is enabled shortly before the export.
   - The request comes from an unusual source IP, region, user agent, or assumed
     role.
   - Export or S3 write permissions were granted shortly before the request.

   The strongest indication of a cross-account export is an `s3BucketOwner` value
   that does not belong to an approved organizational account.

## References

- [AWS: Share an Amazon EBS snapshot](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-modifying-snapshot-permissions.html)
- [AWS API: ModifySnapshotAttribute](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifySnapshotAttribute.html)
- [AWS Service Authorization Reference: Amazon EC2](https://docs.aws.amazon.com/service-authorization/latest/reference/list_ec2.html)
- [AWS API: GetObject](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html)
- [AWS: Enabling CloudTrail event logging for S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/enable-cloudtrail-logging-for-s3.html)
- [AWS: Requesting a DynamoDB table export](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/S3DataExport_Requesting.html)
- [AWS API: ExportTableToPointInTime](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_ExportTableToPointInTime.html)
- [AWS: Logging DynamoDB operations with CloudTrail](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/logging-using-cloudtrail.html)
