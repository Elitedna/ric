import json
import requests
import pandas as pd
from secret import mondayAPIkey
import __db_tools__ as db


def push_with_columns(apikey,
                      board_id,
                      patientid,
                      patient_reg_date,
                      patient_zip,
                      territory,
                      city,
                      ctm_role,
                      state,
                      county,
                      lat,
                      lng
                      ):

    board_id = board_id
    query = 'mutation($myItemName: String!, $columnVals: JSON!) {create_item (board_id: %s, group_id: "1636312626_bree", item_name: $myItemName, column_values: $columnVals) {id}}' % (
        board_id)
    vars = {
        'myItemName': patientid,
        'columnVals': json.dumps({
            'date4': {"date": patient_reg_date},
            'text4': patient_zip,
            'text1': territory,
            'text7': city,
            'text38': ctm_role,
            'text5': state,
            'text8': county,
            'text6': lat,
            'text_1':lng
        })
    }


    headers = {"Authorization": apikey}
    data = {'query': query, 'variables': vars}
    return requests.post(url="https://api.monday.com/v2", json=data, headers=headers)


def drop_unloaded_employees(id,apikey):
    url = "https://api.monday.com/v2?"
    payload="{\"query\":\"mutation {\\n    archive_item (item_id:"  + str(id) + ") {\\n        id\\n    }\\n}\\n    \\n  \",\"variables\":{}}"
    headers = {
      'Authorization': 'Bearer '+ apikey,
      'Content-Type': 'application/json',
      'Cookie': '__cf_bm=rdjkxLZ0Mpm8SMDxm0gHg83k3Mvb3lf0usgl38xOzao-1633556780-0-Acwe5TAE3olBVJPkJYnvMsPUNnWFff3plDcaY69jUyb1SU8C4XvgEcLIktcjfiVIv2eReiFxbslvRu/JcHZgsEI='
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(str(id) + ' Status is:  ',response)


def get_new_employees(apikey):
    url = "https://api.monday.com/v2?"

    payload = "{\"query\":\"\\nquery {\\n  boards (ids:1676275063) {\\n    groups  (ids:\\\"group_title\\\"){\\n    \\titems {\\n        name\\n        id\\n        column_values(ids:[\\\"date4\\\",\\\"text\\\",\\\"text2\\\",\\\"text6\\\"]) {\\n          text\\n          title\\n        }\\n      }\\n    }\\n      \\n    }  \\n      }\\n    \\n  \",\"variables\":{}}"
    headers = {
        'Authorization': 'Bearer '+ apikey,
        'Content-Type': 'application/json',
        'Cookie': '__cf_bm=etrzVwqttbH90zxrLvMNfulSnzE4d7zulFoG6nM4BSM-1633554904-0-AaMoVZs9vgXqBxEZexehkwJSd+s3Gr77O3kfRfX5jJYY824HzzcMHDIhXRbumnocxhwJxPVs+eNWIknyI8upCcQ='
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    content = [i for i in response.json()['data']['boards'][0]['groups'][0]['items']]
    content = [i for i in response.json()['data']['boards'][0]['groups'][0]['items']]
    cleaned = [
        {'name': i['name'], 'start_date': i['column_values'][0]['text'], 'department': i['column_values'][1]['text'],
         'title': i['column_values'][2]['text'], 'monday_id': i['id']} for i in content]

    return pd.DataFrame(cleaned)


def push_employees(apikey, name, date_as_string, department='-', title='-', athena_name='-'):
    board_id = 1676275063
    group_id = "1632344990_something"

    query = 'mutation ($myItemName: String!, $columnVals: JSON!){ create_item (board_id: %s, group_id: "1632344990_something", item_name: $myItemName, column_values:$columnVals) { id } }' % (
        board_id)
    vars = {
        'myItemName': name,
        'columnVals': json.dumps({
            'date4': {'date': date_as_string},
            'text': department,
            'text2': title,
            'text6': athena_name
        }),
        'myGroup_id': group_id
    }


    apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization": apikey}

    data = {'query': query, 'variables': vars}
    r = requests.post(url=apiUrl, json=data, headers=headers)
    return r


def create_error(item_name, boardid):
    query = 'mutation ($itemName: String!){create_item(board_id:%s, group_id: "topics", item_name: $itemName){id}} ' % (boardid)
    var = {
        "itemName": item_name
    }
    return send_query(mondayAPIkey, query, vars=var).json()



def send_query(apiKey, query, vars=None):
    apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization": apiKey}
    if vars != None:
        data = {'query': query, 'variables': vars}
        r = requests.post(url=apiUrl, json=data, headers=headers)
        return r
    else:
        data = {'query': query}
        r = requests.post(url=apiUrl, json=data, headers=headers)
        return r