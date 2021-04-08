## Streaming data from KDA to DynamoDB Table

This Lambda/Python code will be invoked by an Amazon Kinesis Analytics application after it has seen all records associated with a particular row-time value.
If records are emitted to the destination in-application stream with in the Kinesis Analytics application as a tumbling window, this means that this function is invoked per tumbling window trigger.
If records are emitted to the destination in-application stream with in the Kinesis Analytics application as a continuous query or a sliding window, this means your Lambda function will be invoked approximately once per second.

This code will be used as part of a serverless analytics workshop and can also be used with minimal changes for similar use cases.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

