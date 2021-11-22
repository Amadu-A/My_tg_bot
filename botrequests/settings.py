from googletrans import Translator


def get_list_locale() -> dict:
    """
    Функция содержит распарсенный и отсортированный по алфавиту словарь локалей языка с сайта API Hotels
    При необходимости код моджно раскомментировать и обновить словарь.
    :return:
    """

    langu_dict = {
                "ARGENTINA": "es_AR",
                "AUSTRALIA": "en_AU",
                "AUSTRIA": "de_AT",
                "BELIZE": "es_BZ",
                "BENELUX_BE": "nl_BE",
                "BENELUX_DE": "de_BE",
                "BENELUX_FR": "fr_BE",
                "BOLIVIA": "es_BO",
                "BRAZIL": "pt_BR",
                "CANADA_EN": "en_CA",
                "CANADA_FR": "fr_CA",
                "CHILE": "es_CL",
                "CHINA_EN": "en_CN",
                "CHINA_ZH": "zh_CN",
                "COLOMBIA": "es_CO",
                "COSTA_RICA": "es_CR",
                "CROATIA": "hr_HR",
                "CZECH_REPUBLIC": "cs_CZ",
                "DENMARK": "da_DK",
                "ECUADOR": "es_EC",
                "EL_SALVADOR": "es_SV",
                "ESTONIA": "et_EE",
                "FINLAND": "fi_FI",
                "FRANCE": "fr_FR",
                "FRENCH_GUIANA": "fr_GF",
                "GERMANY": "de_DE",
                "GREECE": "el_GR",
                "GUATEMALA": "es_GT",
                "GUYANA": "es_GY",
                "HONDURAS": "es_HN",
                "HONG_KONG_EN": "en_HK",
                "HONG_KONG_ZH": "zh_HK",
                "HUNGARY": "hu_HU",
                "ICELAND": "is_IS",
                "INDIA": "en_IN",
                "INDONESIA_EN": "en_ID",
                "INDONESIA_IN": "in_ID",
                "IRELAND": "en_IE",
                "ISRAEL": "iw_IL",
                "ISRAEL_EN": "en_IL",
                "ITALY": "it_IT",
                "JAPAN_EN": "en_JP",
                "JAPAN_JP": "ja_JP",
                "KOREA_EN": "en_KR",
                "KOREA_KO": "ko_KR",
                "LATVIA": "lv_LV",
                "LITHUANIA": "lt_LT",
                "MALAYSIA_EN": "en_MY",
                "MALAYSIA_MS": "ms_MY",
                "MEXICO_EN": "en_MX",
                "MEXICO_ES": "es_MX",
                "NETHERLANDS": "nl_NL",
                "NEW_ZEALAND": "en_NZ",
                "NICARAGUA": "es_NI",
                "NORWAY": "no_NO",
                "PANAMA": "es_PA",
                "PARAGUAY": "es_PY",
                "PERU": "es_PE",
                "PHILIPPINES": "en_PH",
                "POLAND": "pl_PL",
                "PORTUGAL": "pt_PT",
                "REST_OF_AFRICA_EN": "en_IE",
                "REST_OF_ASIA_EN": "en_AS",
                "REST_OF_EUROPE_EN": "en_IE",
                "REST_OF_LATAM_EN": "en_LA",
                "REST_OF_MIDDLE_EAST_AR": "ar_AE",
                "REST_OF_MIDDLE_EAST_EN": "en_IE",
                "RUSSIAN_FEDERATION": "ru_RU",
                "SINGAPORE": "en_SG",
                "SLOVAKIA": "sk_SK",
                "SOUTH_AFRICA": "en_ZA",
                "SPAIN": "es_ES",
                "SURINAME": "nl_SR",
                "SWEDEN": "sv_SE",
                "SWITZERLAND_DE": "de_CH",
                "SWITZERLAND_FR": "fr_CH",
                "SWITZERLAND_IT": "it_CH",
                "TAIWAN_EN": "en_TW",
                "TAIWAN_ZH": "zh_TW",
                "THAILAND_EN": "en_TH",
                "THAILAND_TH": "th_TH",
                "TURKEY": "tr_TR",
                "UKRAINE": "uk_UA",
                "UNITED_KINGDOM": "en_GB",
                "UNITED_STATES": "en_US",
                "UNITED_STATES_ES": "es_US",
                "URUGUAY": "es_UY",
                "VENEZUELA": "es_VE",
                "VIETNAM_EN": "en_VN",
                "VIETNAM_VN": "vi_VN"
    }
    return langu_dict

def choose_currency() -> list:
    cur_lst = ['USD', 'EUR', 'AED', 'ANG', 'ARS', 'AUD', 'BGN', 'BHD', 'BOB', 'BRL', 'BTN', 'BZD', 'CAD', 'CHF', 'CLP', 'CNY',
     'COP', 'CRC', 'CZK', 'DKK', 'EGP', 'GBP', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HUF', 'IDR', 'ILS', 'INR',
     'ISK', 'JOD', 'JPY', 'KHR', 'KRW', 'KWD', 'KZT', 'LAK', 'LBP', 'LKR', 'MAD', 'MOP', 'MXN', 'MYR', 'NIO', 'NOK',
     'NZD', 'OMR', 'PAB', 'PEN', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RUB', 'SAR', 'SEK', 'SGD', 'SRD', 'THB',
     'TND', 'TRY', 'TWD', 'UAH', 'UYU', 'VND']
    return cur_lst

def translate_google(text: str, dest_google: str='en') -> str:
    try:
        if dest_google == 'ru':
            return text
        translator = Translator()
        newtext = translator.translate(text, dest=dest_google, src='ru')
        return newtext.text
    except Exception:
        return text

def translate_google_converter(text: str) -> str:
    translator = Translator()
    newtext = translator.translate(text, dest='en')
    return newtext.text




