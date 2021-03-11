import boto3

CERTS_BASE_PATH = '/etc/letsencrypt/live'

route53_client = boto3.client('route53')
acm_client = boto3.client('acm', region_name='us-east-1')

def certificate_acm(domain_zone_name, action):
  print('%s certificate to ACM for domain "%s"' % (action, domain_zone_name))
  try:
    issued_certificates = acm_client.list_certificates(
      CertificateStatuses=[
          'ISSUED',
      ],
    )
    domain_cert = [certificate for certificate in issued_certificates['CertificateSummaryList'] if certificate['DomainName'] == domain_zone_name]
    if action == 'UPSERT':
      chain = open(CERTS_BASE_PATH + '/' + domain_zone_name + '/fullchain.pem', 'r').read()
      priv = open(CERTS_BASE_PATH + '/' + domain_zone_name + '/privkey.pem', 'r').read()
      cert = open(CERTS_BASE_PATH + '/' + domain_zone_name + '/cert.pem', 'r').read()

      if len(domain_cert) != 0:
        cert_arn = domain_cert[0]['CertificateArn']
        acm_client.import_certificate(
            CertificateArn=cert_arn,
            Certificate=str.encode(cert),
            PrivateKey=str.encode(priv),
            CertificateChain=str.encode(chain),
        )
      else:
        acm_client.import_certificate(
            Certificate=str.encode(cert),
            PrivateKey=str.encode(priv),
            CertificateChain=str.encode(chain),
        )
    elif action == 'DELETE':
      pass
      # not yet supported, needs additional CloudFront logic to remove certificate there also
      # if len(domain_cert) != 0:
      #   cert_arn = domain_cert['CertificateArn']
      # acm_client.delete_certificate(
      #     CertificateArn=cert_arn
      # )
  except Exception as e:
    print('Importing certificate for domain "%s" failed: %s' % (domain_zone_name, str(e)))