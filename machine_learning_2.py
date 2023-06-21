import pandas as pd
import xgboost as xgb
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn import model_selection
import multiprocessing
import pickle

df_2 = pd.read_excel(r"emlakjet_demo_final_adana_2_all.xlsx")
df_2.drop("Unnamed: 0", axis=1, inplace=True)
df = df_2.copy()

print(df.columns)

n_cpus = multiprocessing.cpu_count()

# Çalışmak istediğimiz sütunları alıyoruz
df = df[["city","district", "neighbourhood", "type", "m", "mg", "room", "age", "heat", "site",
         "furniture", "bath", "floor", "price"]]

# Bağımlı ve Bağımsız değişkenleri ayırıyoruz
X = df.drop(["price"], axis=1)
y = df["price"]

# Eğitim ve Test verisinin ayrılması
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=2000)

X_test.to_csv('X_test_adana_8_all.csv', index=False)
y_test.to_csv('y_test_adana_8_all.csv', index=False)

# GridSearchCV
params = {
    "colsample_bytree": [0.4, 0.5, 0.6],
    "learning_rate": [0.01, 0.02, 0.09],
    "max_depth": [2, 3, 4, 5, 6],
    "n_estimators": [100, 200, 500, 2000]
}

xgb = XGBRegressor()
grid = GridSearchCV(xgb, params, cv=10, n_jobs=n_cpus - 1, verbose=2)
grid.fit(X_train, y_train)

best_params = grid.best_params_
print("En iyi parametreler: ", best_params)

# En uygun parametreleri kullanarak yeni bir model oluşturuyoruz
xgb1 = XGBRegressor(
    colsample_bytree=best_params['colsample_bytree'],
    learning_rate=best_params['learning_rate'],
    max_depth=best_params['max_depth'],
    n_estimators=best_params['n_estimators']
)

# Modeli eğitiyoruz
model_xgb = xgb1.fit(X_train, y_train)

# Tahmin yapıyoruz
pred = model_xgb.predict(X_test)[15:20]
print("Tahminler: ", pred)
print("Gerçek Değerler: ", y_test[15:20])

# Modelin skorunu hesaplıyoruz
test_score = model_xgb.score(X_test, y_test)
train_score = model_xgb.score(X_train, y_train)
print("Test Skoru: ", test_score)
print("Eğitim Skoru: ", train_score)

# Doğrulanmış hata oranını buluyoruz
cv_score = np.sqrt(-1 * (cross_val_score(model_xgb, X_test, y_test, cv=10, scoring='neg_mean_squared_error'))).mean()
print("CV Skoru: ", cv_score)

# Modeldeki parametre önemini görüyoruz
importance = pd.DataFrame({"Importance": model_xgb.feature_importances_}, index=X_train.columns)
print("Parametre Önem Sıralaması:")
print(importance)

# Modeli diske kaydediyoruz
filename = 'finalized_model_adana_8_all.sav'
pickle.dump(model_xgb, open(filename, 'wb'))


"""
import pandas as pd
import xgboost as xgb
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn import model_selection
import multiprocessing
import pickle

df_2 = pd.read_excel(r"emlakjet_demo_final_adana_2.xlsx")
df_2.drop("Unnamed: 0", axis=1, inplace=True)
df = df_2.copy()

print(df.columns)

n_cpus = multiprocessing.cpu_count()

# Çalışmak istediğimiz sütunları alıyoruz
df = df[["district", "neighbourhood", "type", "m", "mg", "room", "age", "heat", "site",
         "furniture", "bath", "floor", "price"]]

# Bağımlı ve Bağımsız değişkenleri ayırıyoruz
X = df.drop(["price"], axis=1)
y = df["price"]

# Eğitim ve Test verisinin ayrılması
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=2000)

X_test.to_csv('X_test_adana_8_.csv', index=False)
y_test.to_csv('y_test_adana_8_.csv', index=False)

# GridSearchCV
params = {
    "colsample_bytree": [0.4, 0.5, 0.6],
    "learning_rate": [0.01, 0.02, 0.09],
    "max_depth": [2, 3, 4, 5, 6],
    "n_estimators": [100, 200, 500, 2000]
}

xgb = XGBRegressor()
grid = GridSearchCV(xgb, params, cv=10, n_jobs=n_cpus - 1, verbose=2)
grid.fit(X_train, y_train)

best_params = grid.best_params_
print("En iyi parametreler: ", best_params)

# En uygun parametreleri kullanarak yeni bir model oluşturuyoruz
xgb1 = XGBRegressor(
    colsample_bytree=best_params['colsample_bytree'],
    learning_rate=best_params['learning_rate'],
    max_depth=best_params['max_depth'],
    n_estimators=best_params['n_estimators']
)

# Modeli eğitiyoruz
model_xgb = xgb1.fit(X_train, y_train)

# Tahmin yapıyoruz
pred = model_xgb.predict(X_test)[15:20]
print("Tahminler: ", pred)
print("Gerçek Değerler: ", y_test[15:20])

# Modelin skorunu hesaplıyoruz
test_score = model_xgb.score(X_test, y_test)
train_score = model_xgb.score(X_train, y_train)
print("Test Skoru: ", test_score)
print("Eğitim Skoru: ", train_score)

# Doğrulanmış hata oranını buluyoruz
cv_score = np.sqrt(-1 * (cross_val_score(model_xgb, X_test, y_test, cv=10, scoring='neg_mean_squared_error'))).mean()
print("CV Skoru: ", cv_score)

# Modeldeki parametre önemini görüyoruz
importance = pd.DataFrame({"Importance": model_xgb.feature_importances_}, index=X_train.columns)
print("Parametre Önem Sıralaması:")
print(importance)

# Modeli diske kaydediyoruz
filename = 'finalized_model_adana_8.sav'
pickle.dump(model_xgb, open(filename, 'wb'))



"""
