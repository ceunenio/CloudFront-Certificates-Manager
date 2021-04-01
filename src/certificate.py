from subprocess import call
from function import notify
from aws import certificate_acm
import os

def create_certificate(ingress_domains, email, env):
  command = ('certbot certonly --agree-tos --manual --manual-public-ip-logging-ok --preferred-challenges http -n -m ' + email + ' --manual-auth-hook=./s3-push.sh --manual-cleanup-hook=./s3-cleanup.sh --expand -d ' + ' -d '.join(ingress_domains)).split()

  output_file = open('certbot_log', 'w')
  code = call(command, stdout=output_file, stderr=output_file, env=env)
  res = open('certbot_log', 'r').read()
  print(res)
  call('rm certbot_log'.split())

  if code != 0:
    message = 'Failed at obtaining certificates for %s' % (str(ingress_domains))
    notify(message, 'danger')
    return

  if code == 0 and "Certificate not yet due for renewal" not in res:
    message = 'Succesfully obtained new certificates for %s' % (str(ingress_domains))
    notify(message, 'good')

  certificate_acm(ingress_domains[0], 'UPSERT')