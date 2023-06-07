import requests
import datetime as datetime
test_interval =  500
server = {'type' : 'API' , 'server' : {'name' : 'uwsgi' }}
cache = {'prov' : 'redis' , 'pubsub' : False , 'high-avail' : True}
reverse_proxy =  {'prov' : False }
framework = 'FLASK'

test_start = datetime.datetime.now()
health_check_list = []
for i in range(test_interval):
    health_check_start = datetime.datetime.now()
    health_check = requests.get('http://localhost:4000/ui/api/health' )
    health_check_status_code = health_check.status_code
    health_check_end = datetime.datetime.now()
    health_check_response_time = health_check_end - health_check_start
    health_check_log = {
        'route': 'health',
        'start' : str(health_check_start) ,
         'end' :   str(health_check_end) ,
         'time' : str(health_check_response_time) , 
         'response_code' : str(health_check_status_code),
        'response' : health_check.json()}

    health_check_list.append(health_check_log)
        
        

create_list = []
for i in range(test_interval):
    create_start = datetime.datetime.now()
    create = requests.post('http://localhost:4000/ui/api/name' , json = {'name' : 'dylan'})
    create_status_code = create.status_code
    create_end = datetime.datetime.now()
    create_response_time = create_end - create_start
    create_log = {
        'route' : 'create', 
        'start' : str(create_start) ,
     'end' :   str(create_end) ,
     'time' : str(create_response_time) , 
     'response_code' : str(create_status_code),
    'response' : create.json()}
    create_list.append(create_log)


List_list = []
for i in range(test_interval):
    List_start = datetime.datetime.now()
    List = requests.get('http://localhost:4000/ui/api/name' )
    List_status_code = List.status_code
    List_end = datetime.datetime.now()
    List_response_time = List_end - List_start
    List_log = {
        'route' : 'List' ,
        'start' : str(List_start) ,
     'end' :   str(List_end) ,
     'time' : str(List_response_time) , 
     'response_code' : str(List_status_code),
               'response' : List.json()}

    List_list.append(List_log)




name_id = create.json()['id']

get_list = []
for i in range(test_interval):
    name_id = create_list[i]['response']['id']
    get = requests.get(f'http://localhost:4000/ui/api/name/{name_id}' , json = {'name' : 'dylan'})
    get_start = datetime.datetime.now()
    get_status_code = get.status_code
    get_end = datetime.datetime.now()
    get_response_time = get_end - get_start
    get_log = {'start' : str(get_start) ,
     'end' :   str(get_end) ,
     'time' : str(get_response_time) , 
     'response_code' : str(get_status_code),
              'response' : get.json(
              )}

    get_list.append(get_log)

update_list = []
for i in range(test_interval):
    name_id = create_list[i]['response']['id']
    update_start = datetime.datetime.now()
    update = requests.put(f'http://localhost:4000/ui/api/name/{name_id}' , json = {'name' : 'bob'})
    update_status_code = update.status_code
    update_end = datetime.datetime.now()
    update_response_time = update_end - update_start
    update_log = {
        'route': 'update' ,
        'start' : str(update_start) ,
     'end' :   str(update_end) ,
     'time' : str(update_response_time) , 
     'response_code' : str(update_status_code)  ,
    'response' : update.json()}

    update_list.append(update_log)

delete_log = []
delete_list = []
for i in range(test_interval):
    name_id = create_list[i]['response']['id']
    delete_start = datetime.datetime.now()
    delete = requests.delete(f'http://localhost:4000/ui/api/name/{name_id}' , json = {'name' : 'bob'})
    delete_status_code = delete.status_code
    delete_end = datetime.datetime.now()
    delete_response_time = delete_end - delete_start
    delete_log = {
        'route' : 'delete',
        'start' : str(delete_start) ,
     'end' :   str(delete_end) ,
     'time' : str(delete_response_time) , 
    'response_code' : str(delete_status_code)  ,
    'response' : delete.text}

    delete_list.append(delete_log)


test_end = datetime.datetime.now()

print(test_end - test_start)
