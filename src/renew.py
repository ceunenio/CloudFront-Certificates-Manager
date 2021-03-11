import time, os
from kubernetes import client, config
from certificate import create_certificate

config.load_incluster_config()
kubernetesv1 = client.ExtensionsV1beta1Api()

EMAIL = os.environ['EMAIL']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

for ingress in kubernetesv1.list_ingress_for_all_namespaces().items:
    print('Refreshing for ingress: %s' % ingress.metadata.name)

    tls = ingress.spec.tls

    hosts = None
    if tls is not None:
        hosts = tls[0].hosts
    
    s3_bucket = None
    annotations = ingress.metadata.annotations
    if 'cloudfront.certmanager/s3-bucket' in annotations:
        s3_bucket = annotations['cloudfront.certmanager/s3-bucket']

    print('-> found tls hosts: %s' % hosts)
    print('-> found cloudfront s3 bucket annotation: %s' % s3_bucket)

    if hosts is not None and s3_bucket is not None:
        create_certificate(hosts, EMAIL, {'S3_BUCKET': s3_bucket, 'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY, 'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID})