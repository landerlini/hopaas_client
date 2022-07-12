# Hopaas Python Client: `hopaas_client`
Hopaas is a service to handle parameter optimization as a service, 
based on RESTful APIs.

`hopaas_client` provides a Python front-end to ease the access to the service, 
embedding the requests in objects and calls for a most Pythonic experience. 

### Install
`hopaas_client` is not released, yet. Still, it can be installed from source as :

```bash
pip install git+https://github.com/landerlini/hopaas_client.git
```

### Configuration 
The first time you run `hopaas_client` it will prompt you for the server address 
and port to be used, and the API token associated to your own account. 

Sometimes (for example for batch jobs) this can be annoying. 
In order to configure `hopaas_client` manually you can create the file `.hopaasrc`
```bash
vim `python -c "import hopaas_client; import os.path; print(os.path.dirname(hopaas_client.__file__))"`/.hopaasrc
```

The configuration file should look like:
```ini
[server]
address = <http[s]://your-server.your-domain.com>
port = <80 or 443>

[auth]
api_token = <your API token>
```




