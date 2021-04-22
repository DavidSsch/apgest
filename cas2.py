from pulp import *
import pandas as pd
from pandas import *
from pandas import ExcelFile


#R = Prix de référence international
#H = Taux d'hummidité maximum en %
#E = Proportion max endomagée
#N = Proportion de matière non orga max
#D = Densité min exigée t/m^3


### DATAS ###

df = pd.read_excel("silos.xls", nrows=11)

silo = list(df['Silo'])

humidity = dict(zip(silo, df['humidity']))
density = dict(zip(silo, df['density']))
dommage = dict(zip(silo, df['dommage']))
non_organic = dict(zip(silo, df['non-organic']))
quantity = dict(zip(silo, df['quantity']))

print(humidity, density, dommage, non_organic, quantity)


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

## MODEL pour un client (for i ), apres faudra utisé for i for j ##

model = LpProblem(name="Ferme_MH_optimisation", sense=LpMaximize)

X = LpVariable.dicts('quantité', silo, cat='Continuous')
Y = LpVariable('oui/non', lowBound=None, upBound=None, cat='Binary')

R = 63
# (R*1.15) - (0.5*H) - E - N + (5*D)

model += lpSum([(R*1.15) - (0.5*humidity[i]) - dommage[i] - non_organic[i] + (5 * density[i]) for i in silo])

#model += lpSum([(R*1.15) - (0.5*humidity[i, c]) - dommage[i, c] - non_organic[i, c] + (5 * density[i, c]) for i in silo for c in clients])

### CONSTRAINTS ###



# (Σ (Hi1* Σyi)) / Σyi < 0.13  besoin de la moyenne ou ca calcul direct????

model += lpSum([humidity[j] * X[j] for j in silo]) <= 0.13, "HumidityMaximum"

model += lpSum([density[j] * X[j] for j in silo]) >= 0.84, "DensityMin"

model += lpSum([dommage[j] * X[j] for j in silo]) <= 0.02, "DommageMaximum"

model += lpSum([non_organic[j] * X[j] for j in silo]) <= 0.02, "Non_organicMaximum"


### Contrainte de quantité

model += lpSum([quantity[j] * X[j] for j in silo]) >= 1350, "QuantityMinimum"

model += lpSum([quantity[j] * X[j] for j in silo]) <= 1500, "QuantityMaximum"


model.solve()
print("Status:", LpStatus[model.status])






