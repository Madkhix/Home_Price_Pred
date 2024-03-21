import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn import model_selection
import multiprocessing
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from sklearn.preprocessing import PolynomialFeatures

df_2 = pd.read_excel(r"emlakjet_demo_final_adana_2_all.xlsx")
df_2.drop("Unnamed: 0", axis=1, inplace=True)
df = df_2.copy()

print(df.columns)

# Visualize views between numeric variables
plt.figure(figsize=(10,8))
sns.heatmap(df.corr(), cmap="RdBu")
plt.title("Correlations Between Variables", size=15)
plt.show()

n_cpus = multiprocessing.cpu_count()

# Çalışmak istediğimiz sütunları alıyoruz
important_num_cols = list(df.corr()["price"][(df.corr()["price"] > 0.50) | (df.corr()["price"] < -0.50)].index)
cat_cols = ["city","district", "neighbourhood", "type", "m", "mg", "room", "age", "heat", "site",
             "furniture", "bath", "floor"]
important_cols = important_num_cols + cat_cols
print(important_cols)

df = df[important_cols]

print("Missing Values by Column")
print("-"*30)
print(df.isna().sum())
print("-"*30)
print("TOTAL MISSING VALUES:",df.isna().sum().sum())

sns.pairplot(df[important_num_cols])

plt.figure(figsize=(10,8))
sns.jointplot(x=df["city"], y=df["price"], kind="kde")
sns.jointplot(x=df["district"], y=df["price"], kind="kde")
sns.jointplot(x=df["neighbourhood"], y=df["price"], kind="kde")
sns.jointplot(x=df["type"], y=df["price"], kind="kde")
sns.jointplot(x=df["type"], y=df["price"], kind="kde")
sns.jointplot(x=df["m"], y=df["price"], kind="kde")
sns.jointplot(x=df["mg"], y=df["price"], kind="kde")
sns.jointplot(x=df["room"], y=df["price"], kind="kde")
sns.jointplot(x=df["age"], y=df["price"], kind="kde")
sns.jointplot(x=df["heat"], y=df["price"], kind="kde")
sns.jointplot(x=df["site"], y=df["price"], kind="kde")
sns.jointplot(x=df["furniture"], y=df["price"], kind="kde")
sns.jointplot(x=df["bath"], y=df["price"], kind="kde")
sns.jointplot(x=df["floor"], y=df["price"], kind="kde")
plt.show()

# Bağımlı ve Bağımsız değişkenleri ayırıyoruz
X = df.drop(["price"], axis=1)
y = df["price"]

# X = pd.get_dummies(X, columns=cat_cols)

# important_num_cols.remove("price")

# scaler = StandardScaler()
# X[important_num_cols] = scaler.fit_transform(X[important_num_cols])

print(X.head())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def rmse_cv(model):
    rmse = np.sqrt(-cross_val_score(model, X, y, scoring="neg_mean_squared_error", cv=5)).mean()
    return rmse
    

def evaluation(y, predictions):
    mae = mean_absolute_error(y, predictions)
    mse = mean_squared_error(y, predictions)
    rmse = np.sqrt(mean_squared_error(y, predictions))
    r_squared = r2_score(y, predictions)
    return mae, mse, rmse, r_squared

def save(model, name):
    X_test.to_csv('X_test_'+name+'13_all.csv', index=False)
    y_test.to_csv('y_test_'+name+'13_all.csv', index=False)
    filename = name+'_13_all.sav'
    pickle.dump(model, open(filename, 'wb'))

# Machine Learning Models
models = pd.DataFrame(columns=["Model","MAE","MSE","RMSE","R2 Score","RMSE (Cross-Validation)"])

# Linear Regression
lin_reg = LinearRegression()
model_Linear = lin_reg.fit(X_train, y_train)
predictions = lin_reg.predict(X_test)
save(model_Linear, 'model_Linear')

mae, mse, rmse, r_squared = evaluation(y_test, predictions)
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2 Score:", r_squared)
print("-"*30)
rmse_cross_val = rmse_cv(lin_reg)
print("RMSE Cross-Validation:", rmse_cross_val)

new_row = {"Model": "LinearRegression","MAE": mae, "MSE": mse, "RMSE": rmse, "R2 Score": r_squared, "RMSE (Cross-Validation)": rmse_cross_val}
models = models.append(new_row, ignore_index=True)

# Ridge Regression
ridge = Ridge()
model_ridge = ridge.fit(X_train, y_train)
predictions = ridge.predict(X_test)
save(model_ridge, 'model_ridge')

mae, mse, rmse, r_squared = evaluation(y_test, predictions)
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2 Score:", r_squared)
print("-"*30)
rmse_cross_val = rmse_cv(ridge)
print("RMSE Cross-Validation:", rmse_cross_val)

new_row = {"Model": "Ridge","MAE": mae, "MSE": mse, "RMSE": rmse, "R2 Score": r_squared, "RMSE (Cross-Validation)": rmse_cross_val}
models = models.append(new_row, ignore_index=True)

# Lasso Regression
lasso = Lasso()
model_lasso = lasso.fit(X_train, y_train)
predictions = lasso.predict(X_test)
save(model_lasso, 'model_lasso')

mae, mse, rmse, r_squared = evaluation(y_test, predictions)
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2 Score:", r_squared)
print("-"*30)
rmse_cross_val = rmse_cv(lasso)
print("RMSE Cross-Validation:", rmse_cross_val)

new_row = {"Model": "Lasso","MAE": mae, "MSE": mse, "RMSE": rmse, "R2 Score": r_squared, "RMSE (Cross-Validation)": rmse_cross_val}
models = models.append(new_row, ignore_index=True)

# Elastic Net
elastic_net = ElasticNet()
model_elastic = elastic_net.fit(X_train, y_train)
predictions = elastic_net.predict(X_test)
save(model_elastic, 'model_elastic')

mae, mse, rmse, r_squared = evaluation(y_test, predictions)
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2 Score:", r_squared)
print("-"*30)
rmse_cross_val = rmse_cv(elastic_net)
print("RMSE Cross-Validation:", rmse_cross_val)

new_row = {"Model": "ElasticNet","MAE": mae, "MSE": mse, "RMSE": rmse, "R2 Score": r_squared, "RMSE (Cross-Validation)": rmse_cross_val}
models = models.append(new_row, ignore_index=True)

# Support Vector Machines
svr = SVR(C=100000)
model_Svr =svr.fit(X_train, y_train)
predictions = svr.predict(X_test)
save(model_Svr, 'model_Svr')

mae, mse, rmse, r_squared = evaluation(y_test, predictions)
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2 Score:", r_squared)
print("-"*30)
rmse_cross_val = rmse_cv(svr)
print("RMSE Cross-Validation:", rmse_cross_val)

new_row = {"Model": "SVR","MAE": mae, "MSE": mse, "RMSE": rmse, "R2 Score": r_squared, "RMSE (Cross-Validation)": rmse_cross_val}
models = models.append(new_row, ignore_index=True)

# Random Forest Regressor
random_forest = RandomForestRegressor(n_estimators=100)
model_random = random_forest.fit(X_train, y_train)
predictions = random_forest.predict(X_test)
save(model_random, 'model_random')

mae, mse, rmse, r_squared = evaluation(y_test, predictions)
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2 Score:", r_squared)
print("-"*30)
rmse_cross_val = rmse_cv(random_forest)
print("RMSE Cross-Validation:", rmse_cross_val)

new_row = {"Model": "RandomForestRegressor","MAE": mae, "MSE": mse, "RMSE": rmse, "R2 Score": r_squared, "RMSE (Cross-Validation)": rmse_cross_val}
models = models.append(new_row, ignore_index=True)

# XGBoost Regressor
xgb = XGBRegressor(n_estimators=1000, learning_rate=0.01)
model_xgb = xgb.fit(X_train, y_train)
predictions = xgb.predict(X_test)
save(model_xgb, 'model_xgb')

mae, mse, rmse, r_squared = evaluation(y_test, predictions)
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2 Score:", r_squared)
print("-"*30)
rmse_cross_val = rmse_cv(xgb)
print("RMSE Cross-Validation:", rmse_cross_val)

new_row = {"Model": "XGBRegressor","MAE": mae, "MSE": mse, "RMSE": rmse, "R2 Score": r_squared, "RMSE (Cross-Validation)": rmse_cross_val}
models = models.append(new_row, ignore_index=True)

# Polynomial Regression (Degree=2)
poly_reg = PolynomialFeatures(degree=2)
X_train_2d = poly_reg.fit_transform(X_train)
X_test_2d = poly_reg.transform(X_test)
save(X_train_2d, 'model_poly')

lin_reg = LinearRegression()
lin_reg.fit(X_train_2d, y_train)
predictions = lin_reg.predict(X_test_2d)

mae, mse, rmse, r_squared = evaluation(y_test, predictions)
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2 Score:", r_squared)
print("-"*30)
rmse_cross_val = rmse_cv(lin_reg)
print("RMSE Cross-Validation:", rmse_cross_val)

new_row = {"Model": "Polynomial Regression (degree=2)","MAE": mae, "MSE": mse, "RMSE": rmse, "R2 Score": r_squared, "RMSE (Cross-Validation)": rmse_cross_val}
models = models.append(new_row, ignore_index=True)

# Model Comparison
sort_models = models.sort_values(by="RMSE (Cross-Validation)")
print(sort_models)

plt.figure(figsize=(12,8))
sns.barplot(x=models["Model"], y=models["RMSE (Cross-Validation)"])
plt.title("Models' RMSE Scores (Cross-Validated)", size=15)
plt.xticks(rotation=30, size=12)
plt.show()
