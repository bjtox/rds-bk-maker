import subprocess
import boto3
import sys
import configparser
from codecs import open
from os.path import expanduser
import os
from datetime import datetime


import boto3
from optparse import OptionParser
import json

def getCurrentTime():
  i = datetime.now()
  return i.strftime('[%Y-%m-%d %H:%M:%S]')


def pushToS3(bucket, key_path, key_name, json):
  s3 = boto3.client('s3', region_name='eu-west-1')
  key = key_path+key_name
  try:
    response = s3.put_object(
      Body=bytes(json),
      Bucket=bucket,
      Key=key,
    )
    return True
  except Exception as e:
    print e
    return False

def get_back_up(user, password, host, db, tunneling):
  if tunneling["enable"]:
    print(getCurrentTime()+" - Tunneling It has been enabled by the bastion Host: "+ tunneling["bastion_host"])
    result = os.popen('ssh -i %s %s@%s \'mysqldump -u %s -p${%s} -h %s %s \' > /dev/null 2>&1' % (
      tunneling["key_pair"],
      tunneling["bastion_user"],
      tunneling["bastion_host"],
      user,
      password,
      host,db)).read()
  else:
    result = os.popen('mysqldump -u %s -p%s -h %s %s > /dev/null 2>&1' % (user, password, host, db)).read()

  return result

def mycallback(x):
  print('mycallback is called with')

def main():
  time = getCurrentTime()
  usage = "usage: %prog [options] arg"
  parser = OptionParser()
  parser.add_option("-j", "--config-file", dest="config_file", help="pass a json file with specification", metavar="CONFIG-FILE")

  (options, args) = parser.parse_args()
  if not options.config_file:  # if filename is not given
    parser.error('Config file not given')

  config_file = options.config_file

  with open(config_file) as data_file:
    data = json.load(data_file)

  print(getCurrentTime()+" Wait, db dumping started for "+data["connection"]["database"]+" schema... ")


  result = pushToS3(
    data["s3Location"]["bucket"],
    data["s3Location"]["key_path"],
    time+'-'+data["s3Location"]["key_name"],
    get_back_up(
      data["connection"]["user"],
      data["connection"]["password"],
      data["connection"]["host"],
      data["connection"]["database"],
      data["tunneling"]
    )
  )

  if result:
    print(getCurrentTime()+" - Db dumping done on a S3 Bucket Named: "+data["s3Location"]["bucket"]+" -> with this Key: "+data["s3Location"]["key_path"]+data["s3Location"]["key_name"])
  else:
    print(getCurrentTime()+" Db dumping failed!")
