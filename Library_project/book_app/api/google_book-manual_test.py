import requests


def get_api_books_from_google(i, title='', author=''):
    query = ''
    if title != '' and author != '':
        query = 'intitle:'+title+'+'+'inauthor:'+author
    elif title == '':
        query = 'inauthor:'+author
    elif author == '':
        query = 'intitle:'+title
    params = {"q": query}
    url = 'https://www.googleapis.com/books/v1/volumes'
    response = requests.get(url, params=params)
    response_dict = response.json()
    return response_dict['items'][i]['volumeInfo'],  response_dict['items']


def check_field_exist_in_api_data(items_volumeInfo_data, final_field):
    field_list = ['publishedDate', 'industryIdentifiers', 'authors',
                  'language', 'pagecount', 'canonicalVolumeLink']
    checking_function_list = [check_date, check_ISBN_is_13, check_author_quantity,
                              check_language, check_page_count, check_url]
    if final_field in items_volumeInfo_data:
        for el in range(len(field_list)):
            if final_field == field_list[el]:
                return checking_function_list[el](items_volumeInfo_data, final_field)
        return items_volumeInfo_data[final_field]
    elif final_field not in items_volumeInfo_data:
        return None


def check_date(data, field):
    if len(data[field]) <= 4:  # if pub_date has only 4 digit
        return data[field] + '-01-01'
    elif len(data[field]) <= 7:  # if pub_date has only 4 digit
        return data[field] + '-01'


def check_ISBN_is_13(data, field):
    for index in range(len(data[field])):
        if data[field][index]['type'] == 'ISBN_13':
            return data[field][index]['identifier']
        elif data[field][index]['type'] != 'ISBN_13':
            continue
    else:
        return data[field][0]['identifier']


def check_author_quantity(data, field):
    author_list = ''
    for author in data[field]:
        if len(data[field]) > 1:
            author_list += author
            author_list += ', '
        elif len(data[field]) == 1:
            author_list += author

    return author_list


def check_page_count(data, field):
    return data[field]


def check_url(data, field):
    return data[field]


def check_language(data, field):
    return data[field]


print(check_field_exist_in_api_data(get_api_books_from_google(8, title='w pustyni i w puszczy')[0],
                                    'industryIdentifiers'))