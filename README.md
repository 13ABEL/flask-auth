# flask-auth

> most of this is based on [this repo](https://github.com/lepture/flask-oauthlib)
Getting started:
Make sure to add a yaml config file (config.yaml) to the project root
-> it should be formated like this and include your credentials for:
1. mongodb

```
secrets: {
  mongoDB: {
    user: <username>,
    password: <password>
  } 
}
```

https://medium.com/@ratrosy/building-a-basic-authorization-server-using-authorization-code-flow-c06866859fb1
https://github.com/michaelawyu/auth-server-sample/