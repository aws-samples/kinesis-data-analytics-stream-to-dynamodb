# An Amazon Kinesis Analytics application will invoke this function after it has seen determined it has seen all records associated with a
# particular rowtime value.
# If records are emitted to the destination in-application stream with in the Kinesis Analytics application as a tumbling window, this means
# that this function is invoked per tumbling window trigger.
# If records are emitted to the destination in-application stream with in the Kinesis Analytics application as a continuous query or a sliding
# window, this means your Lambda function will be invoked approximately once per second.
#
# This function requires that the output records of the Kinesis Analytics application has a key identifier (row_id) and rowtimestamp (row_timestamp)
# and the output record format type is specified as JSON.
#
# A sample output record from Kinesis Analytics application for this function is as below
# {    "RFID": 6989139522658,    "TollID: 179,    "Date-Month": "JAN",    "Date-Day": 27, "Date-Year": 2019,   "Vehicle_Type: "Car"}
from __future__ import print_function
import boto3
import base64
from json import loads

dynamodb_client = boto3.client('dynamodb')

# The block below creates the DDB table with the specified column names.


try:
    response = dynamodb_client.create_table(
        AttributeDefinitions=
        [
	        {
                'AttributeName': "RFID",
                'AttributeType': 'N'
            },

        ],
        KeySchema=
        [
            {
                'AttributeName': "RFID",
                'KeyType': 'HASH',
            },
        ],
        ProvisionedThroughput=
        {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
        TableName='rfid-toll-data-table'
    )
except dynamodb_client.exceptions.ResourceInUseException:
    # Table is created, skip
    pass


def lambda_handler(event, context):
    payload = event['records']
    output = []
    success = 0
    failure = 0

    for record in payload:
        try:
            # # This block parses the record, and writes it to the DDB table.

            payload = base64.b64decode(record['data'])
            data_item = loads(payload)

            ddb_item = { "RFID": { 'N': str(data_item['RFID']) },
                "TollID": { 'N': str(data_item['TollID']) },
                "COL_DateMonth": { 'S': str(data_item['COL_DateMonth']) },
                "COL_DateDay": { 'N': str(data_item['COL_DateDay']) },
                "COL_DateYear": { 'N': str(data_item['COL_DateYear']) },
                "Vehicle_Type": { 'S': str(data_item['Vehicle_Type']) }
            }
            dynamodb_client.put_item(TableName='rfid-toll-data-table', Item=ddb_item)

            success += 1
            output.append({'recordId': record['recordId'], 'result': 'Ok'})
        except Exception:
            failure += 1
            output.append({'recordId': record['recordId'], 'result': 'DeliveryFailed'})

    print('Successfully delivered {0} records, failed to deliver {1} records'.format(success, failure))
    return {'records': output}
