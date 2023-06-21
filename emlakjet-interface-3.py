import tkinter as tk
from tkinter import ttk
import pandas as pd
from joblib import load
import mysql.connector

# Modeli yükle
model = load("finalized_model_adana_8_all.sav")
# X_test = pd.read_csv('X_test_model_xgb8.csv')
# y_test = pd.read_csv('y_test_model_xgb8.csv')

# print(model.score(X_test, y_test))
# # Modeli kullanarak tahminler yapabilirsiniz
# predictions = model.predict(X_test)


# MySQL veritabanına bağlanma
conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="emlakjet",
  charset="utf8",
  raise_on_warnings = True
)

# Bağlantı üzerinden bir cursor oluşturma
cursor = conn.cursor()

# SQL sorgusunu çalıştırma
query = """
SELECT DISTINCT city, district, neighbourhood
FROM real_estate;
"""
cursor.execute(query)

# Sonuçları alma
adresler = cursor.fetchall()

# Tkinter uygulama penceresi
# Adresler verilerini sözlük yapısına dönüştürme
data_dict = {}
for city, district, neighbourhood in adresler:
    if city not in data_dict:
        data_dict[city] = {}
    if district not in data_dict[city]:
        data_dict[city][district] = []
    data_dict[city][district].append(neighbourhood)
    
# Cursor ve bağlantıyı kapatma
cursor.close()
conn.close()

root = tk.Tk()
root.title("Fiyat Tahmini")

# Şehir ComboBox'ı
city_label = tk.Label(root, text="Şehir:")
city_label.pack()
city_combo = ttk.Combobox(root, values=list(data_dict.keys()))
city_combo.pack()

# İlçe ComboBox'ı
district_label = tk.Label(root, text="İlçe:")
district_label.pack()
district_combo = ttk.Combobox(root)
district_combo.pack()

# Mahalle ComboBox'ı
neighborhood_label = tk.Label(root, text="Mahalle:")
neighborhood_label.pack()
neighborhood_combo = ttk.Combobox(root)
neighborhood_combo.pack()

def on_city_selected(event):
    selected_city = city_combo.get()
    # İlçe combobox'ını güncelle
    district_combo.set('')
    district_combo['values'] = list(data_dict[selected_city].keys())

def on_district_selected(event):
    selected_city = city_combo.get()
    selected_district = district_combo.get()
    # Mahalle combobox'ını güncelle
    neighborhood_combo.set('')
    neighborhood_combo['values'] = data_dict[selected_city][selected_district]

city_combo.bind("<<ComboboxSelected>>", on_city_selected)
district_combo.bind("<<ComboboxSelected>>", on_district_selected)

# Type
type_label = tk.Label(root, text="Type:")
type_label.pack()
type_combo = ttk.Combobox(root, values="Konut")
type_combo.pack()

# Brüt metrekare
mg_label = tk.Label(root, text="Brüt Metrekare:")
mg_label.pack()
mg_entry = ttk.Entry(root)
mg_entry.pack()

# Net metrekare
m_label = tk.Label(root, text="Net Metrekare:")
m_label.pack()
m_entry = ttk.Entry(root)
m_entry.pack()

# Oda sayısı
room_label = tk.Label(root, text="Oda Sayısı:")
room_label.pack()
room_combo = ttk.Combobox(root, values=["3+1", "2+1", "4+1", "1+1", "5+1", "4+2", "5+2", "6+1", "3.5+1", "3+2", "6+2", "2+0", "8+", "2.5+1", "1", "4.5+1", "7+1", "Stüdyo", "2+2", "7+2", "6+3", "7+3", "1.5+1", "5+3", "5", "5+4", "6+4"])
room_combo.pack()

# Bina Yaşı
age_label = tk.Label(root, text="Bina Yaşı:")
age_label.pack()
age_combo = ttk.Combobox(root, values=["0", "1", "2", "3", "4", "5-10", "11-15", "16-20", "21 Ve Üzeri"])
age_combo.pack()

# Isınma
heat_label = tk.Label(root, text="Isınma:")
heat_label.pack()
heat_combo = ttk.Combobox(root, values=["Kombi Doğalgaz", "Klimalı", "Yerden Isıtma", "Merkezi Doğalgaz ", "Merkezi (Pay Ölçer)", "Sobalı", "Isıtma Yok", "Kat Kaloriferi", "Doğalgaz Sobalı", "Merkezi Kömür", "Güneş Enerjisi", "Jeotermal", "Isı Pompası", "Şömine", "Kombi Fueloil", "Merkezi Fueloil", "Kombi Kömür", "VRV", "Elektrikli Radyatör", "Fancoil Ünitesi", "Kombi Katı Yakıt"])
heat_combo.pack()

# site
site_label = tk.Label(root, text="Site İçerisinde Mi?:")
site_label.pack()
site_combo = ttk.Combobox(root, values=["Evet", "Hayır"])
site_combo.pack()

# eşya durumu
furniture_label = tk.Label(root, text="Eşya Durumu:")
furniture_label.pack()
furniture_combo = ttk.Combobox(root, values=["Eşyalı", "Boş"])
furniture_combo.pack()

# banyo sayısı
bath_label = tk.Label(root, text="Banyo Sayısı:")
bath_label.pack()
bath_combo = ttk.Combobox(root, values=["0", "1", "2", "3", "4", "5", "6+"])
bath_combo.pack()

# dairenin katı
floor_label = tk.Label(root, text="Kat:")
floor_label.pack()
floor_combo = ttk.Combobox(root, values=["-1", "-2", "-3", "Bodrum", "Giris", "Giris Dubleks", "Villa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10-20", "21-30", "30-40", "40+", "Cati", "Cati Dubleks"])
floor_combo.pack()


# Fiyat Tahmini sonuç Label'ı
result_label = tk.Label(root, text="")
result_label.pack()

def on_predict_button_click():
    selected_city = city_combo.get()
    selected_district = district_combo.get()
    selected_neighbourhood = neighborhood_combo.get()
    selected_type = type_combo.get()
    selected_m = m_entry.get()
    selected_mg = mg_entry.get()
    selected_room = room_combo.get()
    selected_age = age_combo.get()
    selected_heat = heat_combo.get()
    selected_site = site_combo.get()
    selected_furniture = furniture_combo.get()
    selected_bath = bath_combo.get()
    selected_floor = floor_combo.get()
    # Diğer ComboBox'lardan seçilen değerleri de alın
    
    # selected_city = "adana"
    # selected_district = "cukurova"
    # selected_neighbourhood = "Güzelyalı Mahallesi"
    # selected_type = "Konut"
    # selected_m = "170"
    # selected_mg = "185"
    # selected_room = "3+1"
    # selected_age = "4"
    # selected_heat = "Kombi Doğalgaz"
    # selected_site = "Hayır"
    # selected_furniture = "Boş"
    # selected_bath = "2"
    # selected_floor = "1"
    
    # Seçilen değerlere göre veriyi oluştur
    input_data = pd.DataFrame({"city": [selected_city],
                               "district": [selected_district],
                               "neighbourhood": [selected_neighbourhood],
                               "type": [selected_type],
                               "m": [selected_m],
                               "mg": [selected_mg],
                               "room": [selected_room],
                               "age": [selected_age],
                               "heat": [selected_heat],
                               "site": [selected_site],
                               "furniture": [selected_furniture],
                               "bath": [selected_bath],
                               "floor": [selected_floor],
                               })
    # city.xlsx dosyasından 'city' sözlüğü oluşturma
    city_df = pd.read_excel('city.xlsx')
    city_dict = dict(zip(city_df['value'], city_df['key']))
    
    # district.xlsx dosyasından 'district' sözlüğü oluşturma
    district_df = pd.read_excel('district.xlsx')
    district_dict = dict(zip(district_df['value'], district_df['key']))
    
    # neighbourhood.xlsx dosyasından 'neighbourhood' sözlüğü oluşturma
    neighbourhood_df = pd.read_excel('neighbourhood.xlsx')
    neighbourhood_dict = dict(zip(neighbourhood_df['value'], neighbourhood_df['key']))
    
    # type.xlsx dosyasından 'type' sözlüğü oluşturma
    type_df = pd.read_excel('type.xlsx')
    type_dict = dict(zip(type_df['value'], type_df['key']))
    
    # m_dictexcelxlsx dosyasından 'm' sözlüğü oluşturma
    m_df = pd.read_excel('m.xlsx')
    m_dict = dict(zip(m_df['value'], m_df['key']))
    
    # mg.xlsx dosyasından 'mg' sözlüğü oluşturma
    mg_df = pd.read_excel('mg.xlsx')
    mg_dict = dict(zip(mg_df['value'], mg_df['key']))
    
    # room.xlsx dosyasından 'room' sözlüğü oluşturma
    room_df = pd.read_excel('room.xlsx')
    room_dict = dict(zip(room_df['value'], room_df['key']))
    
    # age.xlsx dosyasından 'age' sözlüğü oluşturma
    age_df = pd.read_excel('age.xlsx')
    age_dict = dict(zip(age_df['value'], age_df['key']))
    
    # heat.xlsx dosyasından 'heat' sözlüğü oluşturma
    heat_df = pd.read_excel('heat.xlsx')
    heat_dict = dict(zip(heat_df['value'], heat_df['key']))
    
    # site_dictexcelxlsx dosyasından 'site' sözlüğü oluşturma
    site_df = pd.read_excel('site.xlsx')
    site_dict = dict(zip(site_df['value'], site_df['key']))
    
    # furniture.xlsx dosyasından 'furniture' sözlüğü oluşturma
    furniture_df = pd.read_excel('furniture.xlsx')
    furniture_dict = dict(zip(furniture_df['value'], furniture_df['key']))
    
    # bath.xlsx dosyasından 'bath' sözlüğü oluşturma
    bath_df = pd.read_excel('bath.xlsx')
    bath_dict = dict(zip(bath_df['value'], bath_df['key']))
    
    # floor.xlsx dosyasından 'floor' sözlüğü oluşturma
    floor_df = pd.read_excel('floor.xlsx')
    floor_dict = dict(zip(floor_df['value'], floor_df['key']))

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
    
    input_data_2 = pd.DataFrame(columns=input_data.columns)

    for col in input_data.columns:
        input_data_2[col] = input_data[col].apply(lambda x: all_dicts[col][x] if x in all_dicts[col] else "")

    print(input_data_2)
    
    input_data_2['m'] = input_data['m'].astype(float)
    input_data_2['mg'] = input_data['mg'].astype(float)

    # Model ile tahmin yap
    predicted_price = model.predict(input_data_2)
    
    # Tahmin sonucunu ekrana yazdır
    result_label.configure(text="Tahmin Edilen Fiyat: {:,.0f} TL".format(int(predicted_price[0])))

# Tahmin Et butonu
predict_button = tk.Button(root, text="Tahmin Et", command=on_predict_button_click)
predict_button.pack()

root.mainloop()


def outCity():
    import tkinter as tk
    from tkinter import ttk
    import pandas as pd
    from joblib import load
    import mysql.connector

    # Modeli yükle
    model = load("finalized_model_adana_8_all_outCity.sav")
    # X_test = pd.read_csv('X_test_model_xgb10.csv')
    # y_test = pd.read_csv('y_test_model_xgb10.csv')

    # print(model.score(X_test, y_test))
    # # Modeli kullanarak tahminler yapabilirsiniz
    # predictions = model.predict(X_test)


    # MySQL veritabanına bağlanma
    conn = mysql.connector.connect(
      host="localhost",
      user="root",
      password="root",
      database="emlakjet",
      charset="utf8",
      raise_on_warnings = True
    )

    # Bağlantı üzerinden bir cursor oluşturma
    cursor = conn.cursor()

    # SQL sorgusunu çalıştırma
    query = """
    SELECT DISTINCT city, district, neighbourhood
    FROM real_estate;
    """
    cursor.execute(query)

    # Sonuçları alma
    adresler = cursor.fetchall()

    # Tkinter uygulama penceresi
    # Adresler verilerini sözlük yapısına dönüştürme
    data_dict = {}
    for city, district, neighbourhood in adresler:
        if city not in data_dict:
            data_dict[city] = {}
        if district not in data_dict[city]:
            data_dict[city][district] = []
        data_dict[city][district].append(neighbourhood)
        
    # Cursor ve bağlantıyı kapatma
    cursor.close()
    conn.close()

    root = tk.Tk()
    root.title("Fiyat Tahmini")

    # Şehir ComboBox'ı
    city_label = tk.Label(root, text="Şehir:")
    city_label.pack()
    city_combo = ttk.Combobox(root, values=list(data_dict.keys()))
    city_combo.pack()

    # İlçe ComboBox'ı
    district_label = tk.Label(root, text="İlçe:")
    district_label.pack()
    district_combo = ttk.Combobox(root)
    district_combo.pack()

    # Mahalle ComboBox'ı
    neighborhood_label = tk.Label(root, text="Mahalle:")
    neighborhood_label.pack()
    neighborhood_combo = ttk.Combobox(root)
    neighborhood_combo.pack()

    def on_city_selected(event):
        selected_city = city_combo.get()
        # İlçe combobox'ını güncelle
        district_combo.set('')
        district_combo['values'] = list(data_dict[selected_city].keys())

    def on_district_selected(event):
        selected_city = city_combo.get()
        selected_district = district_combo.get()
        # Mahalle combobox'ını güncelle
        neighborhood_combo.set('')
        neighborhood_combo['values'] = data_dict[selected_city][selected_district]

    city_combo.bind("<<ComboboxSelected>>", on_city_selected)
    district_combo.bind("<<ComboboxSelected>>", on_district_selected)

    # Type
    type_label = tk.Label(root, text="Type:")
    type_label.pack()
    type_combo = ttk.Combobox(root, values="Konut")
    type_combo.pack()

    # Brüt metrekare
    mg_label = tk.Label(root, text="Brüt Metrekare:")
    mg_label.pack()
    mg_entry = ttk.Entry(root)
    mg_entry.pack()

    # Net metrekare
    m_label = tk.Label(root, text="Net Metrekare:")
    m_label.pack()
    m_entry = ttk.Entry(root)
    m_entry.pack()

    # Oda sayısı
    room_label = tk.Label(root, text="Oda Sayısı:")
    room_label.pack()
    room_combo = ttk.Combobox(root, values=["3+1", "2+1", "4+1", "1+1", "5+1", "4+2", "5+2", "6+1", "3.5+1", "3+2", "6+2", "2+0", "8+", "2.5+1", "1", "4.5+1", "7+1", "Stüdyo", "2+2", "7+2", "6+3", "7+3", "1.5+1", "5+3", "5", "5+4", "6+4"])
    room_combo.pack()

    # Bina Yaşı
    age_label = tk.Label(root, text="Bina Yaşı:")
    age_label.pack()
    age_combo = ttk.Combobox(root, values=["0", "1", "2", "3", "4", "5-10", "11-15", "16-20", "21 Ve Üzeri"])
    age_combo.pack()

    # Isınma
    heat_label = tk.Label(root, text="Isınma:")
    heat_label.pack()
    heat_combo = ttk.Combobox(root, values=["Kombi Doğalgaz", "Klimalı", "Yerden Isıtma", "Merkezi Doğalgaz ", "Merkezi (Pay Ölçer)", "Sobalı", "Isıtma Yok", "Kat Kaloriferi", "Doğalgaz Sobalı", "Merkezi Kömür", "Güneş Enerjisi", "Jeotermal", "Isı Pompası", "Şömine", "Kombi Fueloil", "Merkezi Fueloil", "Kombi Kömür", "VRV", "Elektrikli Radyatör", "Fancoil Ünitesi", "Kombi Katı Yakıt"])
    heat_combo.pack()

    # site
    site_label = tk.Label(root, text="Site İçerisinde Mi?:")
    site_label.pack()
    site_combo = ttk.Combobox(root, values=["Evet", "Hayır"])
    site_combo.pack()

    # eşya durumu
    furniture_label = tk.Label(root, text="Eşya Durumu:")
    furniture_label.pack()
    furniture_combo = ttk.Combobox(root, values=["Eşyalı", "Boş"])
    furniture_combo.pack()

    # banyo sayısı
    bath_label = tk.Label(root, text="Banyo Sayısı:")
    bath_label.pack()
    bath_combo = ttk.Combobox(root, values=["0", "1", "2", "3", "4", "5", "6+"])
    bath_combo.pack()

    # dairenin katı
    floor_label = tk.Label(root, text="Kat:")
    floor_label.pack()
    floor_combo = ttk.Combobox(root, values=["-1", "-2", "-3", "Bodrum", "Giris", "Giris Dubleks", "Villa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10-20", "21-30", "30-40", "40+", "Cati", "Cati Dubleks"])
    floor_combo.pack()


    # Fiyat Tahmini sonuç Label'ı
    result_label = tk.Label(root, text="")
    result_label.pack()

    def on_predict_button_click():
        selected_city = city_combo.get()
        selected_district = district_combo.get()
        selected_neighbourhood = neighborhood_combo.get()
        selected_type = type_combo.get()
        selected_m = m_entry.get()
        selected_mg = mg_entry.get()
        selected_room = room_combo.get()
        selected_age = age_combo.get()
        selected_heat = heat_combo.get()
        selected_site = site_combo.get()
        selected_furniture = furniture_combo.get()
        selected_bath = bath_combo.get()
        selected_floor = floor_combo.get()
        # Diğer ComboBox'lardan seçilen değerleri de alın
        
        # selected_city = "adana"
        # selected_district = "cukurova"
        # selected_neighbourhood = "Güzelyalı Mahallesi"
        # selected_type = "Konut"
        # selected_m = "170"
        # selected_mg = "185"
        # selected_room = "3+1"
        # selected_age = "4"
        # selected_heat = "Kombi Doğalgaz"
        # selected_site = "Hayır"
        # selected_furniture = "Boş"
        # selected_bath = "2"
        # selected_floor = "1"
        
        # Seçilen değerlere göre veriyi oluştur
        input_data = pd.DataFrame({#"city": [selected_city],
                                   "district": [selected_district],
                                   "neighbourhood": [selected_neighbourhood],
                                   "type": [selected_type],
                                   "m": [selected_m],
                                   "mg": [selected_mg],
                                   "room": [selected_room],
                                   "age": [selected_age],
                                   "heat": [selected_heat],
                                   "site": [selected_site],
                                   "furniture": [selected_furniture],
                                   "bath": [selected_bath],
                                   "floor": [selected_floor],
                                   })
        # city.xlsx dosyasından 'city' sözlüğü oluşturma
        city_df = pd.read_excel('city.xlsx')
        city_dict = dict(zip(city_df['value'], city_df['key']))
        
        # district.xlsx dosyasından 'district' sözlüğü oluşturma
        district_df = pd.read_excel('district.xlsx')
        district_dict = dict(zip(district_df['value'], district_df['key']))
        
        # neighbourhood.xlsx dosyasından 'neighbourhood' sözlüğü oluşturma
        neighbourhood_df = pd.read_excel('neighbourhood.xlsx')
        neighbourhood_dict = dict(zip(neighbourhood_df['value'], neighbourhood_df['key']))
        
        # type.xlsx dosyasından 'type' sözlüğü oluşturma
        type_df = pd.read_excel('type.xlsx')
        type_dict = dict(zip(type_df['value'], type_df['key']))
        
        # m_dictexcelxlsx dosyasından 'm' sözlüğü oluşturma
        m_df = pd.read_excel('m.xlsx')
        m_dict = dict(zip(m_df['value'], m_df['key']))
        
        # mg.xlsx dosyasından 'mg' sözlüğü oluşturma
        mg_df = pd.read_excel('mg.xlsx')
        mg_dict = dict(zip(mg_df['value'], mg_df['key']))
        
        # room.xlsx dosyasından 'room' sözlüğü oluşturma
        room_df = pd.read_excel('room.xlsx')
        room_dict = dict(zip(room_df['value'], room_df['key']))
        
        # age.xlsx dosyasından 'age' sözlüğü oluşturma
        age_df = pd.read_excel('age.xlsx')
        age_dict = dict(zip(age_df['value'], age_df['key']))
        
        # heat.xlsx dosyasından 'heat' sözlüğü oluşturma
        heat_df = pd.read_excel('heat.xlsx')
        heat_dict = dict(zip(heat_df['value'], heat_df['key']))
        
        # site_dictexcelxlsx dosyasından 'site' sözlüğü oluşturma
        site_df = pd.read_excel('site.xlsx')
        site_dict = dict(zip(site_df['value'], site_df['key']))
        
        # furniture.xlsx dosyasından 'furniture' sözlüğü oluşturma
        furniture_df = pd.read_excel('furniture.xlsx')
        furniture_dict = dict(zip(furniture_df['value'], furniture_df['key']))
        
        # bath.xlsx dosyasından 'bath' sözlüğü oluşturma
        bath_df = pd.read_excel('bath.xlsx')
        bath_dict = dict(zip(bath_df['value'], bath_df['key']))
        
        # floor.xlsx dosyasından 'floor' sözlüğü oluşturma
        floor_df = pd.read_excel('floor.xlsx')
        floor_dict = dict(zip(floor_df['value'], floor_df['key']))

        all_dicts = {
        #'city': city_dict,
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
        
        input_data_2 = pd.DataFrame(columns=input_data.columns)

        for col in input_data.columns:
            input_data_2[col] = input_data[col].apply(lambda x: all_dicts[col][x] if x in all_dicts[col] else "")

        print(input_data_2)
        
        input_data_2['m'] = input_data['m'].astype(float)
        input_data_2['mg'] = input_data['mg'].astype(float)

        # Model ile tahmin yap
        predicted_price = model.predict(input_data_2)
        
        # Tahmin sonucunu ekrana yazdır
        result_label.configure(text="Tahmin Edilen Fiyat: {:,.0f} TL".format(int(predicted_price[0])))

    # Tahmin Et butonu
    predict_button = tk.Button(root, text="Tahmin Et", command=on_predict_button_click)
    predict_button.pack()

    root.mainloop()

