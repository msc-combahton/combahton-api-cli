<h1 align="center">combahton Command Line (cbcli) 🤖</h1>

CLI to interact with the API of combahton.net

## 🚀 Demo

`cbcli` uses a config.ini in the cwd to store details.
To initialize a configuration, just add your api credentials:

```sh
cbcli config user.email username@example.org
cbcli config user.key dea75f268d6880e2617eb3aa
```

Afterwards interact with the API by using the various available modules:

```sh
# enable flowShieldv3 on 123.123.123.123
cbcli antiddos fv3 123.123.123.123 true
# enable permanent layer 4 mitigation for 123.123.123.132
cbcli antiddos layer4 set-routing 123.123.123.123 permanent
# set layer 7 protection method for example.tld to captcha
cbcli antiddos layer7 domain-add example.tld captcha
# show last 25 ddos incidents for 123.123.123.123
cbcli antiddos incidents single 123.123.123.123
# show last 100 ddos incidents for all ips
cbcli antiddos incidents all
# get antiddos status for specific ip
cbcli antiddos show 123.123.123.123
# get details for specific cloud server contract
cbcli cloud view 609123
```

## 🤝 Contributing

Contributions, issues and feature requests are welcome.<br />
Feel free to check [issues page](issues) if you want to contribute.<br />
