import pandas as pd
import ast, os,uuid

def safe_literal_eval(value):
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError, TypeError, MemoryError):
        return value

def eval_data(df):
    df_copy = df.copy()
    for col in df_copy.columns:
        df[col] = df_copy[col].apply(safe_literal_eval)
    return df

def rename_columns(df):
        
    column_mapping = {
        'name' : 'Dat_nuoc',
        'independent' : 'Doc_lap',
        'status' : 'trang_thai',
        'capital' : 'Thu_do',
        'altSpellings' : 'Cach_viet_thay_the',
        'region' : 'Lanh_tho',
        'area' : 'Dien_tich',
        'maps' : 'Ban_do',
        'timezones' : 'Mui_gio',
        'continents' : 'Luc_dia',
        'flags' : 'Quoc_ky',
        'startOfWeek' : 'Ngay_dau_tuan'
    }
    return df.rename(columns=column_mapping)

def cleanCapitalAndAltSpellings(df):
    def clean_cell(cell):
        cell = cell.split(',') if isinstance(cell, str) else cell
        if isinstance(cell, list):
            return ' | '.join(map(str, cell))
        else:
            return None
    if 'capital' in df.columns:
        df['capital'] = df['capital'].apply(clean_cell)
    if 'altSpellings' in df.columns:
        df['altSpellings'] = df['altSpellings'].apply(clean_cell)
    return df

def processLatlng(df):
    def extract_latlng(value):
        value = value['latlng'] if isinstance(value, dict) and 'latlng' in value else value
        lat, lng = None, None
        if isinstance(value, list) and len(value) == 2:
            lat, lng = value[0], value[1]
        elif isinstance(value, str):
            try:
                lat, lng = map(float, value.split(','))
            except ValueError:
                pass
        return pd.Series({'lat': lat, 'lng': lng})
    captitalInfo_index = df.columns.get_loc('capitalInfo')
    latling_info = df['capitalInfo'].apply(extract_latlng)
    for col in ['lat', 'lng']:
        df.insert(captitalInfo_index + 1, col , latling_info[col])
    return df

def processLanguages(df):
    print(type(df['languages']))
    df['su_dung_tieng_anh'] = df['languages'].apply(
        lambda x: 'eng' in x if isinstance(x, dict) else False
    )
    return df

def processTranslations(df):
    df_expendef = df['translations'].apply(pd.Series)
    translation_index = df.columns.get_loc('translations')
    for col in df_expendef.columns:
        df.insert(translation_index + 1, col, df_expendef[col])
    return df

def processGetGooleMapsLink(df):
    def get_google_maps_link(row):
        # print((row['googleMaps']))
        if pd.notna(row) and isinstance(row, dict):
            return row['googleMaps']
        return None
    df['google_maps_link'] = df['maps'].apply(get_google_maps_link)
    return df

def processGetFirstTimezone(df):
    def extract_first_timezone(value):
        if isinstance(value, list) and len(value) >   0:
            return value[0]
        return None
    df['first_timezone'] = df['timezones'].apply(extract_first_timezone)
    return df
def processFlagsSvg(df):
    def get_svg_link(row):
        if pd.notna(row) and isinstance(row, dict):
            return row['svg']
        return None
    df['flag_svg_link'] = df['flags'].apply(get_svg_link)
    return df

def processCreate_quoc_gia_id(df):
    def create_quoc_gia_name(name):
        # name là dict chứa 'common' và 'official'
        if isinstance(name, dict):
            common = name.get('common', '')
            official = name.get('official', '')
            return f"{common}_{official}"
        return ''
    df_name = df['name'].apply(create_quoc_gia_name)
    hashed_namespace = uuid.UUID("9a5963f8-5a5c-4b8c-aa46-1068af074546")
    df['quoc_gia_id'] = df_name.apply(lambda x: str(uuid.uuid5(hashed_namespace, x)))
    return df

def processCurrencies(df):
    currencies = pd.DataFrame(df['currencies'])
    if not currencies.empty:
        currencies.columns = [f'currency_{col}' for col in currencies.columns]
        df = pd.concat([df, currencies], axis=1)
    currencies.to_csv('trusted/currencies.csv', index=False, encoding='utf-8')

def processAll(df):
    df = eval_data(df)
    df = cleanCapitalAndAltSpellings(df)
    df = processLatlng(df)
    df = processLanguages(df)
    df = processTranslations(df)
    df = processGetGooleMapsLink(df)
    df = processGetFirstTimezone(df)
    df = processFlagsSvg(df)
    df = processCreate_quoc_gia_id(df)
    processCurrencies(df)
    df = rename_columns(df)
    return df