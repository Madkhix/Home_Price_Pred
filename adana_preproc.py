import pandas as pd
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="emlakjet",
  charset="utf8",
  raise_on_warnings = True
)

df = pd.read_sql('SELECT * FROM real_estate', con=db)

# Closing MySQL connection
db.close()

# removing unnecessary data
df.drop("date", axis = 1, inplace = True)
df.drop("up_date", axis = 1, inplace = True)
df.drop('rsID', axis=1, inplace=True)
df.drop('title', axis=1, inplace=True)
df.drop('links', axis=1, inplace=True)
df.drop('city', axis=1, inplace=True)

print(df.head(5))

print(df)

df_2 = df.rename(columns = {"0":"price",
                     "1":"neighbourhood",
                     "2":"district",
                     "3":"mg",
                     "4":"m",
                     "5":"room",
                     "6":"age",
                     "7":"floor",
                     "8":"topFloor",
                     "9":"heat",
                     "10":"bath",
                     "11":"furniture",
                     "12":"site",
                     "13":"credit",
                     "14":"titleDeed",
                     "15":"type",
                     "16":"category",
                     "17":"usingStatus",
                     "18":"investment"})

#examining our data
print(df_2.head())
print(df_2.columns)
print(df_2.neighbourhood.value_counts())


# 0
# String conversion
df_2['price'] = df_2['price'].astype(str)

# examining the price regime
print(df_2.price.value_counts())
# Remove "TL" character
df_2['price'] = df_2['price'].str.replace('TL', '')

# Remove "." character
df_2['price'] = df_2['price'].str.replace('.', '')
print(df_2.price.value_counts())

# Removal of non-numeric characters
# df_2['price'] = df_2['price'].str.replace(r'arrow_downward|%\d+', '', regex=True)

# print(df_2.price.value_counts())

# 1
# examine our 'mg' data
print(df_2.mg.value_counts())
# removing the places that say m2.
df_2["mg"] = df_2.mg.str[:-3]

# 2
# examining 'm' data
print(df_2.m.value_counts())
# m2 yazan yerleri kaldırıyoruz.
df_2["m"] = df_2.m.str[:-3]

# 3
# reviewing our room numbers
# removing the places that say "Oda"
print(df_2.room.value_counts())
df_2.loc[df_2.room == "1 Oda", "room"] = "1" 
df_2.loc[df_2.room == "5 Oda", "room"] = "5" 
df_2.loc[df_2.room == "8+ Oda", "room"] = "8+" 
df_2.loc[df_2.room == "9+ Oda", "room"] = "9+" 
df_2.loc[df_2.room == "Stüdyo", "room"] = "1" 


# 4
# examine building ages
print(df_2.age.value_counts())
# we change the building age written like "0 (Yeni)"
df_2.loc[df_2.age == "0 (Yeni)", "age"] = "0"


# 5
#examining floor
print(df_2.floor.value_counts())
# remove those whose number is unknown
df_2 = df_2[df_2['floor'] != ""]
# edit the data
df_2.loc[df_2.floor == "Yüksek Giriş", "floor"] = "Giris"
df_2.loc[df_2.floor == "Düz Giriş", "floor"] = "Giris"
df_2.loc[df_2.floor == "Müstakil.Kat", "floor"] = "Giris"
df_2.loc[df_2.floor == "Bahçe Katı", "floor"] = "Giris"
df_2.loc[df_2.floor == "Villa Tipi", "floor"] = "Villa"
df_2.loc[df_2.floor == "Bahçe Dublex", "floor"] = "Giris Dubleks"
df_2.loc[df_2.floor == "Yüksek Bodrum", "floor"] = "Bodrum"
df_2.loc[df_2.floor == "Tam Bodrum.Kat", "floor"] = "Bodrum"
df_2.loc[df_2.floor == "Yarı Bodrum", "floor"] = "Bodrum"
df_2.loc[df_2.floor == "Çatı Dubleks", "floor"] = "Cati Dubleks"
df_2.loc[df_2.floor == "Çatı Katı", "floor"] = "Cati"

df_2.loc[df_2.floor == "1.Kat", "floor"] = "1"
df_2.loc[df_2.floor == "2.Kat", "floor"] = "2"
df_2.loc[df_2.floor == "3.Kat", "floor"] = "3"
df_2.loc[df_2.floor == "4.Kat", "floor"] = "4"
df_2.loc[df_2.floor == "5.Kat", "floor"] = "5"
df_2.loc[df_2.floor == "6.Kat", "floor"] = "6"
df_2.loc[df_2.floor == "7.Kat", "floor"] = "7"
df_2.loc[df_2.floor == "8.Kat", "floor"] = "8"
df_2.loc[df_2.floor == "9.Kat", "floor"] = "9"


df_2.loc[df_2.floor == "10-20.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "10.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "11.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "12.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "13.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "14.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "15.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "16.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "17.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "18.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "19.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "20.Kat", "floor"] = "10-20"

df_2.loc[df_2.floor == "21.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "22.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "23.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "24.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "25.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "26.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "27.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "28.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "29.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "30.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "20-30.Kat", "floor"] = "21-30"

df_2.loc[df_2.floor == "31.Kat", "floor"] = "30-40"
df_2.loc[df_2.floor == "33.Kat", "floor"] = "30-40"
df_2.loc[df_2.floor == "34.Kat", "floor"] = "30-40"
df_2.loc[df_2.floor == "40+.Kat", "floor"] = "40+"

df_2.loc[df_2.floor == "30-40.Kat", "floor"] = "30-40"

df_2.loc[df_2.floor == "Kot 1 (-1).Kat" , "floor"] = "-1" 
df_2.loc[df_2.floor == "Kot 2 (-2).Kat" , "floor"] = "-2" 
df_2.loc[df_2.floor == "Kot 3 (-3).Kat" , "floor"] = "-3" 

print(df_2.floor.value_counts())

#examine the topFloor
print(df_2.topFloor.value_counts())

# examine types of residential heating
print(df_2.heat.value_counts())


# we write 0 instead of "None" or "Yok" for bathroom properties
print(df_2.bath.value_counts())
df_2.loc[df_2.bath == "Yok", "bath"] = '0'
#df_2.loc[df_2.bath == "6+", "bath"] = 6
# remove those whose number is not specific
df_2 = df_2[df_2['bath'] != ""]
print(df_2.bath.value_counts())


# examine the different titles within the furniture tag
print(df_2.furniture.unique())
# we are looking at how many data items are empty or null
print(df_2.furniture.value_counts())
# eşyalı ya da boş olduğunu belirtmeyen evleri boş olarak alıyoruz
df_2.loc[df_2.furniture == "", "furniture"] = "Boş" 
print(df_2.furniture.value_counts())

# konutların site içerisinde olup olmadığını kontrol ediyoruz
print(df_2.site.value_counts())

# konutların krediye uygun olup olmadığını kontrol ediyoruz
print(df_2.credit.value_counts())
# bilinmiyor olan veri türlerini krediye uygun değile çeviriyoruz
df_2.loc[df_2.credit == "Bilinmiyor", "credit"] = "Krediye Uygun Değil" 
df_2.loc[df_2.credit == "KREDIYE UYGUN", "credit"] = "Krediye Uygun" 

# titleDeed bilnimeyen birçok veri olduğu için bunları veri setimizden kaldırıyoruz
print(df_2.titleDeed.value_counts())
df_2.drop("titleDeed", axis = 1, inplace = True)

# emlakların türünü inceliyoruz
print(df_2.type.value_counts())

# emlakların satılık ya da kiralık durumlarını inceliyoruz
print(df_2.category.value_counts())

# emlakların kullanım durumu
print(df_2.usingStatus.value_counts())


# yatırıma uygunluğu bilnimeyen birçok veri olduğu için bunları bilinmiyor olarak yazdırıyoruz
print(df_2.investment.value_counts())
df_2.loc[df_2.investment == "", "investment"] = "Bilinmiyor" 
print(df_2.investment.value_counts())


# yapılan değişiklikleri kaydediyoruz.
a = df_2.to_excel("emlakjet_demo_adana_1.xlsx")

##########################################################################################

import pandas as pd
import joblib

df = pd.read_excel("emlakjet_demo_adana_1.xlsx")
df.drop("Unnamed: 0", axis = 1, inplace = True)

df = df.dropna()

df_2 = df.copy()
df_3 = df.copy()

print(df_2)

# yeni veri setimizin indexlerini inceliyoruz
print(df_2.columns)

# bath verilerini stringe çeviriyoruz
df['bath'] = df['bath'].astype(str)

# df['mg'] = df['mg'].astype(float)
# df['m'] = df['m'].astype(float)

# Dairenin katı ile ilgili düzenleme
print(df.floor.value_counts())

df['floor'] = df['floor'].astype(str)

print(df.topFloor.value_counts())
# df['topFloor'] = df['topFloor'].astype(str)

from sklearn.preprocessing import LabelEncoder

unique_cities = df['city'].unique()
city_encoder = LabelEncoder()
label_encoded_cities = city_encoder.fit_transform(unique_cities)

unique_districts = df['district'].unique()
district_encoder = LabelEncoder()
label_encoded_districts = district_encoder.fit_transform(unique_districts)

# unique values for neighbourhood feature
unique_neighbourhoods = df['neighbourhood'].unique()
neighbourhood_encoder = LabelEncoder()
label_encoded_neighbourhoods = neighbourhood_encoder.fit_transform(unique_neighbourhoods)

# unique values for type feature
unique_types = df['type'].unique()
type_encoder = LabelEncoder()
label_encoded_types = type_encoder.fit_transform(unique_types)

# unique values for m feature
unique_m_values = df['m'].unique()
m_encoder = LabelEncoder()
label_encoded_m = m_encoder.fit_transform(unique_m_values)

# unique values for mg feature
unique_mg_values = df['mg'].unique()
mg_encoder = LabelEncoder()
label_encoded_mg = mg_encoder.fit_transform(unique_mg_values)

# unique values for room feature
unique_rooms = df['room'].unique()
room_encoder = LabelEncoder()
label_encoded_rooms = room_encoder.fit_transform(unique_rooms)

# unique values for age feature
unique_ages = df['age'].unique()
age_encoder = LabelEncoder()
label_encoded_ages = age_encoder.fit_transform(unique_ages)

# unique values for heat feature
unique_heats = df['heat'].unique()
heat_encoder = LabelEncoder()
label_encoded_heats = heat_encoder.fit_transform(unique_heats)

# unique values for site feature
unique_sites = df['site'].unique()
site_encoder = LabelEncoder()
label_encoded_sites = site_encoder.fit_transform(unique_sites)

# unique values for furniture feature
unique_furnitures = df['furniture'].unique()
furniture_encoder = LabelEncoder()
label_encoded_furnitures = furniture_encoder.fit_transform(unique_furnitures)

# unique values for bath feature
unique_baths = df['bath'].unique()
bath_encoder = LabelEncoder()
label_encoded_baths = bath_encoder.fit_transform(unique_baths)

# unique values for floor feature
unique_floors = df['floor'].unique()
floor_encoder = LabelEncoder()
label_encoded_floors = floor_encoder.fit_transform(unique_floors)

# unique values for category feature
unique_category = df['category'].unique()
category_encoder = LabelEncoder()
label_encoded_category = category_encoder.fit_transform(unique_category)

# unique values for credit feature
unique_credit = df['credit'].unique()
credit_encoder = LabelEncoder()
label_encoded_credit = credit_encoder.fit_transform(unique_credit)

# unique values for usingStatus feature
unique_usingStatus = df['usingStatus'].unique()
usingStatus_encoder = LabelEncoder()
label_encoded_usingStatus = usingStatus_encoder.fit_transform(unique_usingStatus)

# unique values for usingStatus feature
unique_investment = df['investment'].unique()
investment_encoder = LabelEncoder()
label_encoded_investment = investment_encoder.fit_transform(unique_investment)

# By performing a transform operation, we accomplish labeling.
df['city'] = city_encoder.transform(df['city'])

# etiketlediğimiz verilerin neler olduğuna bakarız.
print(df_3.city.unique())

# Bu şekilde hepsi için fit_transform işlemi yapıyoruz.
df['district'] = district_encoder.transform(df['district'])
df['neighbourhood'] = neighbourhood_encoder.transform(df['neighbourhood'])
df['type'] = type_encoder.transform(df['type'])
df['m'] = m_encoder.transform(df['m'])
df['mg'] = mg_encoder.transform(df['mg'])
df['room'] = room_encoder.transform(df['room'])
df['age'] = age_encoder.transform(df['age'])
df['heat'] = heat_encoder.transform(df['heat'])
df['site'] = site_encoder.transform(df['site'])
df['furniture'] = furniture_encoder.transform(df['furniture'])
df['bath'] = bath_encoder.transform(df['bath'])
df['floor'] = floor_encoder.transform(df['floor'])
df['category'] = category_encoder.transform(df['category'])
df['credit'] = credit_encoder.transform(df['credit'])
df['usingStatus'] = usingStatus_encoder.transform(df['usingStatus'])
df['investment'] = investment_encoder.transform(df['investment'])

city_dict = dict(zip(unique_cities, label_encoded_cities))
district_dict = dict(zip(unique_districts, label_encoded_districts))
neighbourhood_dict = dict(zip(unique_neighbourhoods, label_encoded_neighbourhoods))
type_dict = dict(zip(unique_types, label_encoded_types))
m_dict = dict(zip(unique_m_values, label_encoded_m))
mg_dict = dict(zip(unique_mg_values, label_encoded_mg))
room_dict = dict(zip(unique_rooms, label_encoded_rooms))
age_dict = dict(zip(unique_ages, label_encoded_ages))
heat_dict = dict(zip(unique_heats, label_encoded_heats))
site_dict = dict(zip(unique_sites, label_encoded_sites))
furniture_dict = dict(zip(unique_furnitures, label_encoded_furnitures))
bath_dict = dict(zip(unique_baths, label_encoded_baths))
floor_dict = dict(zip(unique_floors, label_encoded_floors))

all_dicts = {
'city': city_dict,
'district': district_dict,
'neighbourhood': neighbourhood_dict,
'type': type_dict,
'm': m_dict,
'mg': mg_dict,
'room': room_dict,
'age': age_dict,
'heat': heat_dict,
'site': site_dict,
'furniture': furniture_dict,
'bath': bath_dict,
'floor': floor_dict
}
import openpyxl

for dict_name in all_dicts:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["value", "key"])
    for key, value in all_dicts[dict_name].items():
        ws.append([key, value])
    wb.save(f"{dict_name}.xlsx")

# yapılan değişikliklerle beraber yeni bir excel dosyasına kaydediyoruz.
a = df.to_excel("emlakjet_demo_final_adana_2.xlsx")






"""

import pandas as pd
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="emlakjet",
  charset="utf8",
  raise_on_warnings = True
)

df = pd.read_sql('SELECT * FROM real_estate', con=db)

# MySQL bağlantısını kapatma
db.close()

# gereksiz verileri kaldırıyoruz
df.drop("date", axis = 1, inplace = True)
df.drop("up_date", axis = 1, inplace = True)
df.drop('rsID', axis=1, inplace=True)
df.drop('title', axis=1, inplace=True)
df.drop('links', axis=1, inplace=True)
#df.drop('city', axis=1, inplace=True)

print(df.head(5))

print(df)

df_2 = df.rename(columns = {"0":"price",
                     "1":"neighbourhood",
                     "2":"city",
                     "3":"district",
                     "4":"mg",
                     "5":"m",
                     "6":"room",
                     "7":"age",
                     "8":"floor",
                     "9":"topFloor",
                     "10":"heat",
                     "11":"bath",
                     "12":"furniture",
                     "13":"site",
                     "14":"credit",
                     "15":"titleDeed",
                     "16":"type",
                     "17":"category",
                     "18":"usingStatus",
                     "19":"investment"})

# verilerimizi inceliyoruz
print(df_2.head())
print(df_2.columns)
print(df_2.neighbourhood.value_counts())


# 0
# String dönüşümü
df_2['price'] = df_2['price'].astype(str)

# fiyat verilerini inceliyoruz
print(df_2.price.value_counts())
# "TL" karakterini kaldırma
df_2['price'] = df_2['price'].str.replace('TL', '')

# "." karakterlerini kaldırma
df_2['price'] = df_2['price'].str.replace('.', '')
print(df_2.price.value_counts())

# Sayısal olmayan karakterleri kaldırma
df_2['price'] = df_2['price'].str.replace(r'arrow_downward|%\d+', '', regex=True)

print(df_2.price.value_counts())


# 1
# mg verilerimizi inceliyoruz
print(df_2.mg.value_counts())
# m2 yazan yerleri kaldırıyoruz.
df_2["mg"] = df_2.mg.str[:-3]

# 2
# m verilerimizi inceliyoruz
print(df_2.m.value_counts())
# m2 yazan yerleri kaldırıyoruz.
df_2["m"] = df_2.m.str[:-3]

# 3
# oda sayılarımızı inceliyoruz
# Oda yazan yerleri kaldırıyoruz
print(df_2.room.value_counts())
df_2.loc[df_2.room == "1 Oda", "room"] = "1" 
df_2.loc[df_2.room == "5 Oda", "room"] = "5" 
df_2.loc[df_2.room == "8+ Oda", "room"] = "8+" 
df_2.loc[df_2.room == "9+ Oda", "room"] = "9+" 
df_2.loc[df_2.room == "Stüdyo", "room"] = "1" 


# 4
# bina yaşlarını inceliyoruz
print(df_2.age.value_counts())
# bu şekilde yazan bina yaşını sıfır yapıyoruz
df_2.loc[df_2.age == "0 (Yeni)", "age"] = "0"


# 5
# konut katını inceliyoruz
print(df_2.floor.value_counts())
# sayısı belirli olmayanları kaldırıyoruz
df_2 = df_2[df_2['floor'] != ""]
# verileri düzenliyoruz
df_2.loc[df_2.floor == "Yüksek Giriş", "floor"] = "Giris"
df_2.loc[df_2.floor == "Düz Giriş", "floor"] = "Giris"
df_2.loc[df_2.floor == "Müstakil.Kat", "floor"] = "Giris"
df_2.loc[df_2.floor == "Bahçe Katı", "floor"] = "Giris"
df_2.loc[df_2.floor == "Villa Tipi", "floor"] = "Villa"
df_2.loc[df_2.floor == "Bahçe Dublex", "floor"] = "Giris Dubleks"
df_2.loc[df_2.floor == "Yüksek Bodrum", "floor"] = "Bodrum"
df_2.loc[df_2.floor == "Tam Bodrum.Kat", "floor"] = "Bodrum"
df_2.loc[df_2.floor == "Yarı Bodrum", "floor"] = "Bodrum"
df_2.loc[df_2.floor == "Çatı Dubleks", "floor"] = "Cati Dubleks"
df_2.loc[df_2.floor == "Çatı Katı", "floor"] = "Cati"

df_2.loc[df_2.floor == "1.Kat", "floor"] = "1"
df_2.loc[df_2.floor == "2.Kat", "floor"] = "2"
df_2.loc[df_2.floor == "3.Kat", "floor"] = "3"
df_2.loc[df_2.floor == "4.Kat", "floor"] = "4"
df_2.loc[df_2.floor == "5.Kat", "floor"] = "5"
df_2.loc[df_2.floor == "6.Kat", "floor"] = "6"
df_2.loc[df_2.floor == "7.Kat", "floor"] = "7"
df_2.loc[df_2.floor == "8.Kat", "floor"] = "8"
df_2.loc[df_2.floor == "9.Kat", "floor"] = "9"


df_2.loc[df_2.floor == "10-20.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "10.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "11.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "12.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "13.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "14.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "15.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "16.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "17.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "18.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "19.Kat", "floor"] = "10-20"
df_2.loc[df_2.floor == "20.Kat", "floor"] = "10-20"

df_2.loc[df_2.floor == "21.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "22.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "23.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "24.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "25.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "26.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "27.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "28.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "29.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "30.Kat", "floor"] = "21-30"
df_2.loc[df_2.floor == "20-30.Kat", "floor"] = "21-30"

df_2.loc[df_2.floor == "31.Kat", "floor"] = "30-40"
df_2.loc[df_2.floor == "33.Kat", "floor"] = "30-40"
df_2.loc[df_2.floor == "34.Kat", "floor"] = "30-40"
df_2.loc[df_2.floor == "40+.Kat", "floor"] = "40+"

df_2.loc[df_2.floor == "30-40.Kat", "floor"] = "30-40"

df_2.loc[df_2.floor == "Kot 1 (-1).Kat" , "floor"] = "-1" 
df_2.loc[df_2.floor == "Kot 2 (-2).Kat" , "floor"] = "-2" 
df_2.loc[df_2.floor == "Kot 3 (-3).Kat" , "floor"] = "-3" 

print(df_2.floor.value_counts())

# bina katını inceliyoruz
print(df_2.topFloor.value_counts())

# konut ısıtma türünü inceliyoruz
print(df_2.heat.value_counts())


# banyo sayısında yok yazan yerlere 0 yazıyoruz
print(df_2.bath.value_counts())
df_2.loc[df_2.bath == "Yok", "bath"] = '0'
#df_2.loc[df_2.bath == "6+", "bath"] = 6
# sayısı belirli olmayanları kaldırıyoruz
df_2 = df_2[df_2['bath'] != ""]
print(df_2.bath.value_counts())


# eşyalı etiketi içerisindeki farklı başlıkları inceliyoruz
print(df_2.furniture.unique())
# eşyalı boş ya da null olan kaç veri olduğuna bakıyoruz
print(df_2.furniture.value_counts())
# eşyalı ya da boş olduğunu belirtmeyen evleri boş olarak alıyoruz
df_2.loc[df_2.furniture == "", "furniture"] = "Boş" 
print(df_2.furniture.value_counts())

# konutların site içerisinde olup olmadığını kontrol ediyoruz
print(df_2.site.value_counts())

# konutların krediye uygun olup olmadığını kontrol ediyoruz
print(df_2.credit.value_counts())
# bilinmiyor olan veri türlerini krediye uygun değile çeviriyoruz
df_2.loc[df_2.credit == "Bilinmiyor", "credit"] = "Krediye Uygun Değil" 
df_2.loc[df_2.credit == "KREDIYE UYGUN", "credit"] = "Krediye Uygun" 

# titleDeed bilnimeyen birçok veri olduğu için bunları veri setimizden kaldırıyoruz
print(df_2.titleDeed.value_counts())
df_2.drop("titleDeed", axis = 1, inplace = True)

# emlakların türünü inceliyoruz
print(df_2.type.value_counts())

# emlakların satılık ya da kiralık durumlarını inceliyoruz
print(df_2.category.value_counts())

# emlakların kullanım durumu
print(df_2.usingStatus.value_counts())


# yatırıma uygunluğu bilnimeyen birçok veri olduğu için bunları bilinmiyor olarak yazdırıyoruz
print(df_2.investment.value_counts())
df_2.loc[df_2.investment == "", "investment"] = "Bilinmiyor" 
print(df_2.investment.value_counts())


# yapılan değişiklikleri kaydediyoruz.
a = df_2.to_excel("emlakjet_demo_adana_1_all.xlsx")

##########################################################################################

import pandas as pd
import joblib

df = pd.read_excel("emlakjet_demo_adana_1_all.xlsx")
df.drop("Unnamed: 0", axis = 1, inplace = True)

df = df.dropna()

df_2 = df.copy()
df_3 = df.copy()

print(df_2)

# yeni veri setimizin indexlerini inceliyoruz
print(df_2.columns)

# bath verilerini stringe çeviriyoruz
df['bath'] = df['bath'].astype(str)

# df['mg'] = df['mg'].astype(float)
# df['m'] = df['m'].astype(float)

# Dairenin katı ile ilgili düzenleme
print(df.floor.value_counts())

df['floor'] = df['floor'].astype(str)

print(df.topFloor.value_counts())
# df['topFloor'] = df['topFloor'].astype(str)

from sklearn.preprocessing import LabelEncoder

unique_cities = df['city'].unique()
city_encoder = LabelEncoder()
label_encoded_cities = city_encoder.fit_transform(unique_cities)

unique_districts = df['district'].unique()
district_encoder = LabelEncoder()
label_encoded_districts = district_encoder.fit_transform(unique_districts)

# unique values for neighbourhood feature
unique_neighbourhoods = df['neighbourhood'].unique()
neighbourhood_encoder = LabelEncoder()
label_encoded_neighbourhoods = neighbourhood_encoder.fit_transform(unique_neighbourhoods)

# unique values for type feature
unique_types = df['type'].unique()
type_encoder = LabelEncoder()
label_encoded_types = type_encoder.fit_transform(unique_types)

# unique values for m feature
unique_m_values = df['m'].unique()
m_encoder = LabelEncoder()
label_encoded_m = m_encoder.fit_transform(unique_m_values)

# unique values for mg feature
unique_mg_values = df['mg'].unique()
mg_encoder = LabelEncoder()
label_encoded_mg = mg_encoder.fit_transform(unique_mg_values)

# unique values for room feature
unique_rooms = df['room'].unique()
room_encoder = LabelEncoder()
label_encoded_rooms = room_encoder.fit_transform(unique_rooms)

# unique values for age feature
unique_ages = df['age'].unique()
age_encoder = LabelEncoder()
label_encoded_ages = age_encoder.fit_transform(unique_ages)

# unique values for heat feature
unique_heats = df['heat'].unique()
heat_encoder = LabelEncoder()
label_encoded_heats = heat_encoder.fit_transform(unique_heats)

# unique values for site feature
unique_sites = df['site'].unique()
site_encoder = LabelEncoder()
label_encoded_sites = site_encoder.fit_transform(unique_sites)

# unique values for furniture feature
unique_furnitures = df['furniture'].unique()
furniture_encoder = LabelEncoder()
label_encoded_furnitures = furniture_encoder.fit_transform(unique_furnitures)

# unique values for bath feature
unique_baths = df['bath'].unique()
bath_encoder = LabelEncoder()
label_encoded_baths = bath_encoder.fit_transform(unique_baths)

# unique values for floor feature
unique_floors = df['floor'].unique()
floor_encoder = LabelEncoder()
label_encoded_floors = floor_encoder.fit_transform(unique_floors)

# unique values for category feature
unique_category = df['category'].unique()
category_encoder = LabelEncoder()
label_encoded_category = category_encoder.fit_transform(unique_category)

# unique values for credit feature
unique_credit = df['credit'].unique()
credit_encoder = LabelEncoder()
label_encoded_credit = credit_encoder.fit_transform(unique_credit)

# unique values for usingStatus feature
unique_usingStatus = df['usingStatus'].unique()
usingStatus_encoder = LabelEncoder()
label_encoded_usingStatus = usingStatus_encoder.fit_transform(unique_usingStatus)

# unique values for usingStatus feature
unique_investment = df['investment'].unique()
investment_encoder = LabelEncoder()
label_encoded_investment = investment_encoder.fit_transform(unique_investment)

# transform işlemi yaparak etiketleme yapmış oluruz.
df['city'] = city_encoder.transform(df['city'])

# etiketlediğimiz verilerin neler olduğuna bakarız.

print(df_3.city.unique())

# Bu şekilde hepsi için fit_transform işlemi yapıyoruz.
df['district'] = district_encoder.transform(df['district'])
df['neighbourhood'] = neighbourhood_encoder.transform(df['neighbourhood'])
df['type'] = type_encoder.transform(df['type'])
df['m'] = m_encoder.transform(df['m'])
df['mg'] = mg_encoder.transform(df['mg'])
df['room'] = room_encoder.transform(df['room'])
df['age'] = age_encoder.transform(df['age'])
df['heat'] = heat_encoder.transform(df['heat'])
df['site'] = site_encoder.transform(df['site'])
df['furniture'] = furniture_encoder.transform(df['furniture'])
df['bath'] = bath_encoder.transform(df['bath'])
df['floor'] = floor_encoder.transform(df['floor'])
df['category'] = category_encoder.transform(df['category'])
df['credit'] = credit_encoder.transform(df['credit'])
df['usingStatus'] = usingStatus_encoder.transform(df['usingStatus'])
df['investment'] = investment_encoder.transform(df['investment'])



city_dict = dict(zip(unique_cities, label_encoded_cities))
district_dict = dict(zip(unique_districts, label_encoded_districts))
neighbourhood_dict = dict(zip(unique_neighbourhoods, label_encoded_neighbourhoods))
type_dict = dict(zip(unique_types, label_encoded_types))
m_dict = dict(zip(unique_m_values, label_encoded_m))
mg_dict = dict(zip(unique_mg_values, label_encoded_mg))
room_dict = dict(zip(unique_rooms, label_encoded_rooms))
age_dict = dict(zip(unique_ages, label_encoded_ages))
heat_dict = dict(zip(unique_heats, label_encoded_heats))
site_dict = dict(zip(unique_sites, label_encoded_sites))
furniture_dict = dict(zip(unique_furnitures, label_encoded_furnitures))
bath_dict = dict(zip(unique_baths, label_encoded_baths))
floor_dict = dict(zip(unique_floors, label_encoded_floors))

all_dicts = {
'city': city_dict,
'district': district_dict,
'neighbourhood': neighbourhood_dict,
'type': type_dict,
'm': m_dict,
'mg': mg_dict,
'room': room_dict,
'age': age_dict,
'heat': heat_dict,
'site': site_dict,
'furniture': furniture_dict,
'bath': bath_dict,
'floor': floor_dict
}
import openpyxl

for dict_name in all_dicts:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["value", "key"])
    for key, value in all_dicts[dict_name].items():
        ws.append([key, value])
    wb.save(f"{dict_name}.xlsx")

# yapılan değişikliklerle beraber yeni bir excel dosyasına kaydediyoruz.
a = df.to_excel("emlakjet_demo_final_adana_2_all.xlsx")








"""





