![image](https://user-images.githubusercontent.com/44908794/212040251-8e059593-1f3a-40b5-914d-1d1db081bc88.png)

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

### Minimal example
The following code snippet uses `hopaas` via `hopaas_client` to optimize a BDT.
```python
from sklearn.ensemble import GradientBoostingClassifier as GBDT
from sklearn.datasets import make_classification

# Load the hopaas frontend
import hopaas_client as hpc

# Create the dataset and split it into classification and validation samples
X, y = make_classification(n_samples=10000)
X_train, X_test = X[::2], X[1::2]
y_train, y_test = y[::2], y[1::2]

# Create the study
study = hpc.Study('Iris GBDT v7', properties=dict(
    n_estimators=hpc.suggestions.Int(2,20),
    learning_rate=0.1, 
    max_depth=hpc.suggestions.Int(2,5)
  ),
  sampler=hpc.samplers.TPESampler(),
  pruner=hpc.pruners.MedianPruner()
)

# Iterate over a given number of trials
for iTrial in range(20):
  # Requests a trial to the hopaas server
  with study.trial() as trial:
    # Instanciate a BDT with the parameters suggested by hopaas 
    bdt = GBDT(
        n_estimators=trial.n_estimators, 
        learning_rate=trial.learning_rate,
        max_depth=trial.max_depth
        )
    
    # Train the bdt
    bdt.fit(X_train, y_train)

    # Update the trial with the score of the BDT providing a loss 
    # that hopaas will try to minimize
    trial.loss = 1.-bdt.score(X_test, y_test)
```

## Licence
`hopaas_client` is made available under MIT licence. 
The backend will be released under GPL 3 at a more advanced stage of the development.
