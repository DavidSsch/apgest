from pulp import *
import pandas as pd
from pandas import *
from pandas import ExcelFile



### DATAS ###

df = pd.read_excel("silos.xls", nrows=11)

silo = list(df['Silo'])


humidity = dict(zip(silo, df['humidity']))
density = dict(zip(silo, df['density']))
dommage = dict(zip(silo, df['dommage']))
non_organic = dict(zip(silo, df['non-organic']))
quantity = dict(zip(silo, df['quantity']))
print(silo,humidity, density, dommage, non_organic, quantity)


# DATA CLIENTS #
df = pd.read_excel("clients.xls", nrows=3)

clients = list(df['Client'])

c_humidity = dict(zip(clients, df['humidity']))
c_density = dict(zip(clients, df['density']))
c_dommage = dict(zip(clients, df['dommage']))
c_non_organic = dict(zip(clients, df['non-organic']))
c_quantitymin = dict(zip(clients, df['Qmin']))
c_quantitymax = dict(zip(clients, df['Qmax']))

print(clients, c_density, c_dommage, c_non_organic, c_quantitymax, c_quantitymin, c_humidity)

R =63

## Variables ##

# i fournisseur
# j clients

X = LpVariable.dict('quantité', silo, clients, cat='Continious')


## Model ##

model = LpProblem(name="Ferme_MH_optimisation", sense=LpMaximize)

model += lpSum([X[i, j] * (P-C) for i in silo for j in clients])

### CONSTRAINTS ###

model += lpSum(([X[i, j] * humidity[i]] // X[i, j]) for i in silo for j in clients) <= (c_humidity[j] for j in clients), 'humidity'

model += lpSum([X[i, j] * density[i]] for i in silo for j in clients) <= (c_density[j] for j in clients), 'density'

model += lpSum([X[i, j] * dommage[i]] for i in silo for j in clients) >= (c_dommage[j] for j in clients), 'dommage'

model += lpSum([X[i, j] * non_organic[i]] for i in silo for j in clients) <= (c_non_organic[j] for j in clients), 'nonorganic'



### Contrainte de quantité

model += lpSum([quantity[i] for i in silo]) <= (X[i, j] for i in silo for j in clients), "QuantityMinimum"

model += lpSum([quantity[i] for i in silo]) <= (X[i, j] for i in silo for j in clients), "QuantityMinimum"




