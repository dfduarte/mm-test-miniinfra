# Code challenge

## 1- Abstract

This code challenge is intended only for this process with the MaxMilhas.

This one follows all the scope/guidelines informed in the HR's e-mail.

## 2- How to deploy the Terraform code

The Terraform code here installs the AWS SQS Queue in a specified account by the user.

To successfully run it, you must run the following:

```
$ terraform init

$ AWS_REGION='your desired region' \
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} terraform plan

$ AWS_REGION='your desired region' \
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} terraform apply -auto-approve
```

**WARNING**: I'm assuming at this point you already have a specific IAM user created with bare minimum permissions for SQS and all the required things. That wasn't requested on documentation, that's why!

Considering this is only for show and code test purposes, I wasn't concerned to tight the SQS policies too much, so I used a generic one. The policy follows:

```
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
```

REMEMEBER: A good policy should've a `sqs:Send*` and `sqs:Receive*` policies at bare minimum, for specific `Principals` of a given environment. Again, considering this is just a closed demo, this is not necessary at this point.

The Terraform code will spit out the SQS queue URL's in the output at the end of the process.

## 3- Running the cluster

This is one of the simplest parts. Just run:

```
# To build up your images:
$ AWS_REGION='your desired region' \
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} docker-compose build

# To get everything up and running
$ AWS_REGION='your desired region' \
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} docker-compose up
```

Why passing the variables inline? That's because docker-compose needs this to pass to containers, in order to make `boto3` recognizes the correct IAM account and its policies.

**WARNING**: I'm assuming at this point you already have a specific IAM user created with bare minimum permissions for SQS and all the required things. That wasn't requested on documentation, that's why!

## 4- So, what do we got here How do we test it????

We got 2 different applications with a database:

An API which receives a JSON through a POST. This JSON basically only must have a "suggestion" attribute key followed by a free string value. For example:

```
{'suggestion': 'this is a example of suggestion'}
```

Since the documentation doesn't specify any route name or even a format for the payload, I assumed that's enough.

Therefore, send it by POSTing anything to `/suggestions`. The server will respond on the port `8090`

Eg: http://127.0.0.1:8090/suggestions

You can use cURL or Postman for this task.

You must see a success message as a output. Otherwise, you'll see an error asking for the correct JSON payload/obj.

At the other side, we got another container running a worker, which will collect all the queue, delete the grabbed messages from it and feed an MongoDB (accessible through mongodb:27017 in the cluster).

Again, since it's only for show, this Mongo server don't have any authentication set. BE AWARE TO NOT RUN THIS IN A PROD ENVIRONMENT, SINCE IT CAN HURT IT, you know...

Since the project requirement didn't say anything else (like deal with messages in the Mongo, or even retrieving the documents in the suggestions collection), that's all for it.

All the requirements are described in their respectives requirements.txt and Dockefiles files.

## 5- Some explanations about the bonus requirement: Service discovery

I prefered follow anoter strategy when discovering the SQS queue: Simply using own boto to discover the correct queue and using this info in the worker.

I thought service discovery could be a bit overkill for this kind of task. Also, completely unnecessary and dispensable.

For example: The complexity to set a new Consul server for this kind of project is overkill, this is not the main purpose of it.

Of course, we got Consul-AWS, which can map all the services using Cloud Map to the into the Consul Datacenter. 

Or even use a sidecar for K8s, but again: overkill just to find a queue name, that could be done programatically.

## 6- Tests:

The requirement didn't cover the testing part, which could be perfectly attended by a `shelllinter`, `terratest` or `inspec` or even a `pylint`, or such as `pycharm` as a test for the code.

Also, I'm running out of time these days, and unfortunatelly I wasn't able to properly take care of it. Part of the code has some linting issues, which some of them need to be silenced or taken care.

