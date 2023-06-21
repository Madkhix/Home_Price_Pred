from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, WebDriverException
import pandas as pd
import mysql.connector
import unicodedata
import logging

# Türkiye'nin şehir ve ilçelerini içeren sözlük yapısı
cities = {
    "konya": ["selcuklu", "seydisehir",
              "taskent", "tuzlukcu", "yalihuyuk", "yunak"],

    "kutahya": ["altintas", "aslanapa", "cavdarhisar", "domanic", "dumlupinar", "emet", "gediz", "hisarcik", "kutahya-merkez",
                "pazarlar", "saphane", "simav", "tavsanli"],

    "malatya": ["akcadag", "arapgir", "arguvan", "battalgazi", "darende", "dogansehir", "doganyol", "hekimhan", "kale",
                "kuluncak", "puturge", "yazihan", "yesilyurt"],

    "manisa": ["ahmetli", "akhisar", "alasehir", "demirci", "golmarmara", "gordes", "kirkagac", "koprubasi", "kula",
               "salihli", "sarigol", "saruhanli", "selendi", "soma", "sehzadeler", "turgutlu", "yunusemre"],

    "mardin": ["artuklu", "dargecit", "derik", "kiziltepe", "mazidagi", "midyat", "nusaybin", "omerli", "savur",
               "yesilli"],

    "mersin": ["akdeniz", "anamur", "aydincik", "bozyazi", "camliyayla", "erdemli", "gulnar", "mezitli", "mut",
               "silifke", "tarsus", "toroslar", "yenisehir"],

    "mugla": ["bodrum", "dalaman", "datca", "fethiye", "kavaklidere", "koycegiz", "marmaris", "mentese", "milas",
              "ortaca", "seydikemer", "ula", "yatagan"],

    "mus": ["bulanik", "haskoy", "korkut", "malazgirt", "mus-merkez", "varto"],

    "nevsehir": ["acigol", "avanos", "derinkuyu", "gulsehir", "hacibektas", "kozakli", "nevsehir-merkez", "urgup"],

    "nigde": ["altunhisar", "bor", "camardi", "ciftlik", "nigde-merkez", "ulukisla"],

    "ordu": ["akkus", "altinordu", "aybasti", "camas", "catalpinar", "caybasi", "fatsa", "golkoy", "gulyali",
             "gurgentepe", "ikizce", "kabaduz", "kabatas", "korgan", "kumru", "mesudiye", "persembe", "ulubey", "unye"],

    "osmaniye": ["bahce", "duzici", "hasanbeyli", "kadirli", "osmaniye-merkez", "sumbas", "toprakkale"],

    "rize": ["ardesen", "camlihemsin", "cayeli", "derepazari", "findikli", "guneysu", "hemsin", "ikizdere", "iyidere",
             "kalkandere", "pazar", "rize-merkez"],

    "sakarya": ["adapazari", "akyazi", "arifiye", "erenler", "ferizli", "geyve", "hendek", "karapurcek", "karasu",
                "kaynarca", "kocaali", "pamukova", "sapanca", "serdivan", "sogutlu", "tarakli"],

    "samsun": ["alacam", "asarcik", "atakum", "ayvacik", "bafra", "canik", "carsamba", "havza", "ilkadim", "kavak",
               "ladik", "ondokuzmayis", "salipazari", "tekkekoy", "terme", "vezirkopru", "yakakent"],

    "siirt": ["siirt-merkez", "tillo", "baykan", "eruh", "kurtalan", "pervari", "sirvan"],

    "sinop": ["ayancik", "boyabat", "dikmen", "duragan", "erfelek", "gerze", "sarayduzu", "sinop-merkez", "turkeli"],

    "sivas": ["akincilar", "altinyayla", "divrigi", "dogansar", "gemerek", "golova", "hafik", "imranli", "kangal",
              "koyulhisar", "sivas-merkez", "susehri", "sarkisla", "ulas", "yildizeli", "zara", "gurun"],

    "sanliurfa": ["akcakale", "birecik", "bozova", "ceylanpinar", "eyyubiye", "halfeti", "haliliye", "harran", "hilvan",
                  "karakopru", "siverek", "suruc", "viransehir"],

    "sirnak": ["beytussebap", "cizre", "guclukonak", "idil", "silopi", "sirnak-merkez", "uludere"],

    "tekirdag": ["cerkezkoy", "corlu", "ergene", "hayrabolu", "kapakli", "malkara", "marmara ereglisi", "muratli",
                 "saray", "suleymanpasa", "sarkoy"],

    "tokat": ["almus", "artova", "basciftlik", "erbaa", "niksar", "pazar", "resadiye", "sulusaray", "tokat-merkez", "turhal",
              "yesilyurt", "zile"],

    "trabzon": ["akcaabat", "arakli", "arsin", "besikduzu", "carsibasi", "caykara", "dernekpazari", "duzkoy", "hayrat",
                "koprubasi", "macka", "of", "ortahisar", "surmene", "salpazari", "tonya", "vakfikebir", "yomra"],

    "tunceli": ["cemisgezek", "hozat", "mazgirt", "nazimiye", "ovacik", "pertek", "pulumur", "tunceli-merkez"],

    "usak": ["banaz", "esme", "karahalli", "sivasli", "ulubey", "usak-merkez"],

    "van": ["bahcesaray", "baskale", "caldiran", "catak", "edremit", "ercis", "gevas", "gurpinar", "ipekyolu",
            "muradiye", "ozalp", "saray", "tusba"],

    "yalova": ["altinova", "armutlu", "cinarcik", "ciftlikkoy", "termal", "merkez"],

    "yozgat": ["akdagmadeni", "aydincik", "bogazliyan", "candir", "cayiralan", "cekerek", "kadisehri", "saraykent",
               "sarikaya", "sorgun", "sefaatli", "yenifakili", "yerkoy", "yozgat-merkez"],

    "zonguldak": ["alapli", "caycuma", "devrek", "gokcebey", "kilimli", "kozlu", "eregli", "zonguldak-merkez"]
}

logging.basicConfig(filename="logfile2.txt",format="%(asctime)s %(message)s",filemode="w",level=logging.DEBUG)

logger = logging.getLogger()

def save_to_sql():
    db = mysql.connector.connect(
      host="localhost",
      user="root",
      password="root",
      database="emlakjet",
      charset="utf8"
    )
    cursor = db.cursor()
    sql = "INSERT INTO real_estate (title, price, neighbourhood, city, district, date, mg, m, room, age, floor, topFloor, heat, bath, furniture, site, credit, titleDeed, type, up_date, category, usingStatus, investment, links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # Listelerden döngü ile geçerek verileri tabloya ekliyoruz
    for i in range(len(titles_list)):
        data = (titles_list[i], prices_list[i], neighbourhood_list[i], district_list[i], city_list[i], date_list[i], mg_list[i], m_list[i], room_list[i], age_list[i], floor_list[i], topFloor_list[i], heat_list[i], bath_list[i], furniture_list[i], site_list[i], credit_list[i], titleDeed_list[i], type_list[i], update_list[i], category_list[i], usingStatus_list[i], investment_list[i], url_list[i])
        cursor.execute(sql, data)

    # Verileri veri tabanına kaydediyoruz
    db.commit()

    # Veritabanı bağlantısını kapatıyoruz
    db.close()

def check_value(s, item, lst):
    res_list= []
    #Sayfada yer alan ilan bilgileri kısmındaki tüm div leri gezerek aradığımız bilgiyi bulup listemize ekliyoruz
    #En fazla 12 div olduğu için burada 13 sayısını verdik içerideki döngüde ise isim ve değer olarak div ler 1 ve 2 olarak ayırılıyor bu yüzden orada da range i 3 belirledik
    for i in range(1,13):
        for j in range (1,3):
            try:
                a = driver.find_element(By.XPATH, f'//*[@id="bilgiler"]/div/div[2]/div/div[1]/div[{j}]/div[{i}]/div[1]')
                res_list.append(a.text)            
                if a.text == s:
                    item = driver.find_element(By.XPATH, f'//*[@id="bilgiler"]/div/div[2]/div/div[1]/div[{j}]/div[{i}]/div[2]')
                    lst.append(item.text)
            except (NoSuchElementException):
                pass
    #Aranan eleman bulunmuyorsa listeye boş eleman ekliyoruz
    if s in res_list:
        res_list.append(s)
    else:
        lst.append("")                       
                
options = Options()

# Enable headless mode
options.add_argument('-headless')

# Web sayfasını açma
driver = webdriver.Firefox(options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 5)

#cekmekoy 35. sayfada kalındı
#sayfalardaki tüm linkleri seçmek için boş bir liste
ad_urls=[]
#sadece ilan linkleri için boş bir liste
href = []
new_prices_list = []
for j in cities:
    for k in cities[j]:
        for i in range(1,51,1):
            print(str (j)+"-"+str(k)+"-"+str(i))
            try:
                driver.get("https://www.emlakjet.com/satilik-konut/"+j+"-"+k+"/{0}".format(i)) 
                sleep(2)
                ad_urls.clear()
                href.clear()
            except (WebDriverException) as e:
                print("Sayfa yenilendi WebDriverException")
                logger.exception(e)
                break
            try:
                div = driver.find_element(By.XPATH, '//*[@id="listing-search-wrapper"]/div[1]/a')
                # İlan listesi div elementi var, ilanlar listeleniyor
            except (NoSuchElementException) as e:
                print("Sayfada ilan yok")
                logger.exception(e)
                break
            
            div = driver.find_element(By.XPATH, '//div')
            # locate all the link elements under the tbody element
            links = div.find_elements(By.XPATH, './/a')                
            # iterate over the links and print the href attribute of each one           
            for link in links:
                href.append(link.get_attribute('href'))            
                
            for h in href:             
                if h is not None and h[25:29] == "ilan" and h not in ad_urls:
                    ad_urls.append(h)
            
            for url in ad_urls:
                # boş liste
                titles_list, prices_list, neighbourhood_list, district_list, city_list, date_list, mg_list, m_list, room_list, age_list, floor_list, topFloor_list, heat_list, bath_list, furniture_list, site_list, credit_list, titleDeed_list, type_list, update_list, category_list, usingStatus_list, investment_list, url_list = ([] for i in range(24))
                #boş değişken
                item_date, item_site, item_date, item_mg, item_m, item_room, item_age, item_floor, item_topFloor, item_heat, item_bath, item_bath, item_furniture, item_site, item_credit, item_titleDeed, item_type, item_update, item_category, item_usingStatus, item_investment = ("" for i in range(21))

                print(url)
                try:
                    driver.get(url)
                    element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/head/title")))
                except (TimeoutException, WebDriverException) as e:
                    driver.refresh()
                    print("Sayfa yenilendi Timeout 1")
                    logger.exception(e)
                    continue
                try:
                    # Scroll the element 
                    scroll = driver.find_element(By.XPATH,'//*[@id="bilgiler"]/div')
                    element = driver.find_element(By.CSS_SELECTOR,"span.Gp4epw")
                    driver.execute_script("arguments[0].scrollIntoView();", scroll)
                    driver.execute_script("arguments[0].click();", element)
                except (NoSuchElementException, ElementClickInterceptedException, WebDriverException):
                    driver.refresh()
                    print("Sayfa yenilendi Timeout 2")
                    continue
                
                
                try:
                    item_titles = driver.find_element(By.XPATH,'//*[@id="__next"]/div[3]/div[2]/div[2]/div[1]/h1')
                    item_prices = driver.find_element(By.XPATH,'//*[@id="__next"]/div[3]/div[2]/div[2]/div[2]/div[1]/div')
                    item_neighbourhood = driver.find_element(By.XPATH,'//*[@id="bolge-raporu"]/div/div[2]/div/div/div[3]/div[1]')
                except NoSuchElementException as e:
                    driver.refresh()
                    print("item_neighbourhood err")
                    logger.exception(e)
                    continue
                
                item_district = j
                item_city = k
                
                check_value("İlan Oluşturma Tarihi", item_date, date_list)
                check_value("Brüt Metrekare", item_mg, mg_list)   
                check_value("Net Metrekare", item_m, m_list)
                check_value("Oda Sayısı", item_room, room_list)
                check_value("Binanın Yaşı", item_age, age_list)
                check_value("Bulunduğu Kat", item_floor, floor_list)
                check_value("Binanın Kat Sayısı", item_topFloor, topFloor_list)
                check_value("Isıtma Tipi", item_heat, heat_list)
                check_value("Banyo Sayısı", item_bath, bath_list)
                check_value("Eşya Durumu", item_furniture, furniture_list)
                check_value("Site İçerisinde", item_site, site_list)
                check_value("Krediye Uygunluk", item_credit, credit_list)
                check_value("Tapu Durumu", item_titleDeed, titleDeed_list)
                check_value("Türü", item_type, type_list)
                check_value("İlan Güncelleme Tarihi", item_update, update_list)
                check_value("Kategorisi", item_category, category_list)
                check_value("Kullanım Durumu", item_usingStatus, usingStatus_list)
                check_value("Yatırıma Uygunluk", item_investment, investment_list)
                
                text =  item_titles.text
                clean_text = "".join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn' and c.isascii())
                titles_list.append(clean_text)
                prices_list.append(item_prices.text) 
                neighbourhood_list.append(item_neighbourhood.text)
                district_list.append(item_district)
                city_list.append(item_city)
                url_list.append(url)


                
                # for price in prices_list:
                #     new_price = price.replace('TL', ' TL')
                #     new_prices_list.append(new_price)
                #print(prices_list)
                save_to_sql()
driver.quit()

# dfS = pd.DataFrame(zip(titles_list, prices_list, neighbourhood_list, district_list, city_list, date_list, mg_list, m_list, room_list, age_list, floor_list, topFloor_list, heat_list, bath_list, furniture_list, site_list, credit_list, titleDeed_list, type_list, update_list, category_list, usingStatus_list, investment_list), 
#                    columns=['Title', 'Price', 'Neighbourhood', 'District', 'City', 'Publish Date', 'Gross Square Meter', 'Square Meter', 'Number of Rooms', 'Age of The Building', 'Floor of The Building', 'Top Floor of The Building', 'Building Heat', 'Number of Bathrooms', 'Furniture', 'Site', 'Credit', 'Title Deed', 'Type', 'Update', 'Category', 'Using Status', 'Invesment'])
# a = dfS.to_excel("Emlakjet_output.xlsx",sheet_name='home_sell') 