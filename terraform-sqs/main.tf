resource "aws_sqs_queue" "maxmilhas_queue" {
  name                      = "maxmilhas"
  delay_seconds             = 0
  max_message_size          = 262143
  message_retention_seconds = 86400
  visibility_timeout_seconds = 1
  kms_master_key_id         = "alias/aws/sqs"
  kms_data_key_reuse_period_seconds = 300


  tags = {
    Purpose = "maxmilhas"
  }
}

resource "aws_sqs_queue_policy" "maxmilhas_queue" {
  queue_url = "${aws_sqs_queue.maxmilhas_queue.id}"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqspolicy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:*",
      "Resource": "${aws_sqs_queue.maxmilhas_queue.arn}",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${aws_sqs_queue.maxmilhas_queue.arn}"
        }
      }
    }
  ]
}
POLICY
}

output "maxmilhas_queue_addr" {
  value = "${aws_sqs_queue.maxmilhas_queue.id}"
}