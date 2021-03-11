# CloudFront Certificates Manager

CloudFront Certificates manager runs every week and requests new Let's Encrypt certificates if needed, they will be uploaded to ACM. The initial setup of CloudFront still needs to be done, but after that certificates will be renewed automatically.

[![DockerHub Badge](https://dockeri.co/image/ceunenio/cloudfront-certmanager)](https://hub.docker.com/r/ceunenio/cloudfront-certmanager)

## Environment Variables
The configmap contains environment variables which can be used to configure Slack notifications and are used for Let's Encrypt certficate requests. The `SLACK_WEBHOOK` variable is optional.

* EMAIL
* SLACK_WEBHOOK
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY

## AWS Policy
Attach following policy to a user that has above AWS keys.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Action": [
                "acm:ImportCertificate",
                "acm:ListCertificates"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:PutObjectACL",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::*/.well-known/acme-challenge/*"
            ]
        }
    ]
}
```

## Usage
Fill in the variables of the ConfigMap and Secret first.

```
kubectl apply -f kubernetes/
```

## Ingress Annotations
Only ingresses with following annotation will be picked up.

* cloudfront.certmanager/s3-bucket