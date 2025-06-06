import uuid, os
import pandas as pd
import ast

def safe_literal_eval(val):
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError, TypeError, MemoryError):
        return val

def rename_columns_df(df_input):
    df = df_input.copy()

    cols_to_eval = [
        'name', 'currencies', 'capital', 'altSpellings', 'languages', 'translations', 
        'demonyms', 'flags', 'coatOfArms', 'capitalInfo', 'borders', 'timezones', 'idd', 
        'gini', 'car', 'postalCode', 'continents'
    ]

    for col in cols_to_eval:
        if col in df.columns:
            df[col] = df[col].apply(safe_literal_eval)
            
    df = df.rename(
        columns = {
            'name' : 'ten', 
            'independent' : 'doc lap',
            'status' : 'trang thai',
            'unMember' : 'khong phai thanh vien',
            'currencies' : 'tien te',
            'capital' : 'thu do', 
            'altSpellings' : 'cach viet thay the', 
            'region' : 'lanh tho',
            'subregion' : 'tieu vung',
            'languages' : 'ngon ngu', 
            'landlocked' : 'khong giap bien',
            'borders' : 'bien gioi quoc gia',
            'area' : 'dien tich',
            'demonyms' : 'ten goi cu dan',
            'translations' : 'ban dich', 
            'flag' : 'quoc ky_unicode',
            'population' : 'dan so',
            'car' : 'o to',
            'timezones' : 'mui gio',
            'continents' : 'luc dia', 
            'flags' : 'co', 
            'coatOfArms' : 'huy hieu', 
            'startOfWeek' : 'ngay dau tien cua tuan',
            'capitalInfo' : 'thong tin thu do', 
            'postalCode' : 'ma buu dien' 
        }
    )
    return df

def list_to_pipe_string(lst):
    if isinstance(lst, list):
        return '|'.join(map(str, lst)) 
    return lst 
class CURRENCIES:
    def __init__(self, df):
        self.df = df.copy() 

    def process_capitalAndAltSpellings(self):
        if 'thu do' in self.df.columns:
            self.df['thu do'] = self.df['thu do'].apply(lambda cell: " | ".join(map(str, cell)) if isinstance(cell, list) else cell)
        if 'cach viet thay the' in self.df.columns:
            self.df['cach viet thay the'] = self.df['cach viet thay the'].apply(lambda cell: " | ".join(map(str, cell)) if isinstance(cell, list) else cell)


    def process_latlng(self):
        if 'thong tin thu do' in self.df.columns:
            def extract_lat_lng(capital_info_dict):
                lat, lng = None, None
                if isinstance(capital_info_dict, dict) and 'latlng' in capital_info_dict:
                    latlng_list = capital_info_dict['latlng']
                    if isinstance(latlng_list, list) and len(latlng_list) == 2:
                        lat, lng = latlng_list[0], latlng_list[1]
                return pd.Series([lat, lng], index=['kinhdo', 'vido'])
            
            latlng_data = self.df['thong tin thu do'].apply(extract_lat_lng)
            self.df['kinhdo'] = latlng_data['kinhdo']
            self.df['vido'] = latlng_data['vido']

    def process_languages(self):
        if 'ngon ngu' in self.df.columns:
            self.df['su_dung_tieng_anh'] = self.df['ngon ngu'].apply(
                lambda langs_dict: 'eng' in langs_dict if isinstance(langs_dict, dict) else False
            )

    def process_translations(self):
        if 'ban dich' in self.df.columns:
            df_expended = self.df['ban dich'].apply(pd.Series)
            self.df = pd.concat([self.df.drop('ban dich', axis=1), df_expended], axis=1)
            self.df

    def process_maps(self):
        if 'maps' in self.df.columns:
            def extract_googleMaps(map_dict):
                if isinstance(map_dict, dict):
                    return map_dict.get('googleMaps', None)
                return None
            self.df['google_maps_url'] = self.df['maps'].apply(extract_googleMaps)
            self.df.drop(columns=['maps'], inplace=True)

    def process_timezone(self):
        if 'mui gio' in self.df.columns:
            def extract_first_timezone(timezones_list):
                if isinstance(timezones_list, list) and len(timezones_list) > 0:
                    return timezones_list[0]
                return None
            self.df['mui_gio_dau_tien'] = self.df['mui gio'].apply(extract_first_timezone)
            self.df.drop(columns=['mui gio'], inplace=True)

    def process_flags(self):
        if 'co' in self.df.columns:
            def extract_svg_image(flag_dict):
                if isinstance(flag_dict, dict):
                    return flag_dict.get('svg', None)
                return None
            self.df['co_svg_url'] = self.df['co'].apply(extract_svg_image)
            self.df.drop(columns=['co'], inplace=True)

    def process_create_country_id(self):
        if 'ten' in self.df.columns:
            def create_id_from_name_dict(name_dict):
                country_str_parts = []
                if isinstance(name_dict, dict):
                    country_str_parts.append(name_dict.get('common', ''))
                    country_str_parts.append(name_dict.get('official', ''))
                elif isinstance(name_dict, str): 
                    country_str_parts.append(name_dict)
                
                country_identifier = "".join(filter(None, country_str_parts)) 
                if not country_identifier:
                    return None 

                hashed_namespace = uuid.UUID('9a5963f8-5a5c-4b8c-aa46-1068af074546')
                return str(uuid.uuid5(hashed_namespace, country_identifier))
            self.df['country_id'] = self.df['ten'].apply(create_id_from_name_dict)
    
    def process_all(self):
        self.process_capitalAndAltSpellings()
        self.process_latlng()
        self.process_languages()
        self.process_translations()
        self.process_maps()
        self.process_timezone()
        self.process_flags()
        self.process_create_country_id()
        return self.df 

def process_transform(csv_path):
    os.makedirs('/opt/airflow/trusted', exist_ok=True)

    raw_df = pd.read_csv(csv_path)
    
    df_renamed_cleaned = rename_columns_df(raw_df)


    cols_for_data_processing = [
        'ten', 'ccn3', 'cca3', 'doc lap', 'trang thai', 'thu do', 
        'cach viet thay the', 'lanh tho', 'dien tich', 'maps', 'mui gio', 
        'luc dia', 'co', 'ngay dau tien cua tuan', 'thong tin thu do', 
        'ngon ngu', 'ban dich' 
    ]
    
    data_df_for_currencies = pd.DataFrame()
    for col_name in cols_for_data_processing:
        if col_name in df_renamed_cleaned.columns:
            data_df_for_currencies[col_name] = df_renamed_cleaned[col_name]
        else:
            data_df_for_currencies[col_name] = None

    df_renamed_cleaned.to_csv('/opt/airflow/trusted/countries.csv', index=False)
    
    currencies_processor = CURRENCIES(data_df_for_currencies)
    processed_data_df = currencies_processor.process_all()
    
    processed_data_df.to_csv('/opt/airflow/trusted/country_currency.csv', index=False)