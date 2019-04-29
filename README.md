# Password Storage

Features:
* Stores password dumps for easy wins.
* Great searching interface.
* List accounts by username, password, dump.
* Easily enter new dumps

## Example usage

* Configure pwdquery.yaml

```yaml
server: 127.0.0.1
```

* `pwdquery [identifier]`

```
Cracked passwords for <identifier>:
passw0rd123
password
ruby1

Uncracked hashes for <identifier>:
09f7e02f1290be211da707a266f153b3
5ac78c81d1b3c28c8db48f57dd2b90b3
```

* `pwdquery -p [password]`

```
Identifiers for password <password>:
maxh@maxh.io
mpharle@g.clemson.edu
```

* `pwdquery -q [identifier]`

```
passw0rd123
password
ruby1
```

* `pwdquery -q --uncracked [identifier]`

```
09f7e02f1290be211da707a266f153b3
5ac78c81d1b3c28c8db48f57dd2b90b3
```

## Tables

_Dump_

| Column     | Type |
|------------|------|
| id         | ID   |
| identifier | TEXT |
| email      | TEXT |
| hash       | TEXT |
| password   | TEXT |
