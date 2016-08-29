# BK Maker

## Installation
```
pip install bkmaker
```


Python script to facilitate backups from your rds instance directly on S3

You have to provide a config file in json format.

```
{
  "name":"Name",
  "type":"mysql",
  "connection":{
    "host":"host connection address",
    "user":"db_user",
    "password":"user_password",
    "database":"database_name"
  },
  "s3Location":{
    "bucket": "bucket_name",
    "key_path": "key_path_of_file",//in case of no path leave blank
    "key_name": "name_of_file"
  },
  "tunneling":{
    "enable" : false,
    "key_pair" : "/local/path/of/key.pem",
    "bastion_user" : "user_connetion_bastiona",
    "bastion_host" : "host_address_bastion"
  }
}
```

NOTE:

Beta Version*
* exporting only from mysql, missing other commands for other dabases

Commands
```
bkmaker --config-file test.json'connection_name' => make a sql file (in RAM) and push it on s3
```
Feel free to contribute or comment my code!