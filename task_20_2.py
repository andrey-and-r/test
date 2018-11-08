# -*- coding: utf-8 -*-
'''
Задание 20.2

Создать функцию send_commands_threads, которая запускает функцию send_commands из задания 19.3 на разных устройствах в параллельных потоках.

Параметры функции send_commands_threads надо определить самостоятельно.
Должна быть возможность передавать параметры show, config, filename функции send_commands.

Функция send_commands_threads возвращает словарь с результатами выполнения команд на устройствах:

* ключ - IP устройства
* значение - вывод с выполнением команд

'''
import yaml
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import time
from itertools import repeat
import os

commands = [
    'logging 10.255.255.1', 'logging buffered 20010', 'no logging console'
]
command = 'sh ip int br'

device = 'devices.yaml'
#filename = 'config.txt'

def send_show_command (devices, command):
    result = {}
    print ('show')
    print (devices)
    print (command)
    for device in devices:
        print (device)
        with ConnectHandler(**device, fast_cli=True) as ssh:
            print ('Connection device: {} Start time -> {}'.format(device['ip'], datetime.now().time()))
            ssh.enable()
            result[device['ip']]=ssh.send_command(command)
            print ('Connection device: {} End time -> {}'.format(device['ip'], datetime.now().time()))
    return result

def send_config_commands (device, commands):
    result = {}
    print ('config')
    with ConnectHandler(**device, fast_cli=True) as ssh:
        ssh.enable()
        result[device['ip']]=ssh.send_config_set(commands)
    return result

def send_command_from_file (device, filename):
    result = {}
    print ('filename')
    with ConnectHandler(**device, fast_cli=True ) as ssh:
        ssh.enable()
        result[device['ip']]=ssh.send_config_from_file(filename)
    return result

#def send_commands (device, config=None, show=None, filename=None):
def send_commands (device, **d):
    print (d)
    for k in d.keys():
        if k == 'show':
    #if show:
            print ('show_show')
            return send_show_command (device, d['show'])
    #elif config:
        #print ('config_config')
        #return send_config_commands (device, config)
    #elif filename:
        #print ('filename_filename')
        #return send_command_from_file (device, filename)

def threads_conn (function, devices, command_=show):
    with ThreadPoolExecutor(max_workers=2) as executor:
        f_result = executor.map(function, devices, repeat(command_))
        #result_dict = {}
        #for item in list(f_result):
            #result_dict.update(item)
    #return result_dict
    return list(f_result)

#def threads_conn (function, devices):
#    all_results = []
#    with ThreadPoolExecutor(max_workers=2) as executor:
#        future_ssh = [executor.submit(function, device) for device in devices]
#        for f in as_completed(future_ssh):
#            all_results.append(f.result())
#    return all_results

#devices = yaml.load(open(device))
#for item in devices['routers']:
    #print (item)
    #print (devices['routers'])
#print (threads_conn(send_show_command, devices['routers'], command = command))
#print (threads_conn(send_commands([item for item in devices['routers']], show=command), devices['routers'], command_ = command))
#print (threads_conn([send_commands(item, show = command) for item in devices['routers']], devices['routers'], command_ = command))
    #print (threads_conn(send_commands(item, filename = 'config.txt'), com = 'config.txt'))
#with open (device) as f:
#    for item in yaml.load(f)['routers']:
        #print (item)
#        print (send_commands(item, show=command))
        #print (send_commands(item, show=command))
        #print (send_commands(item, filename))
with open (device) as f:
    item = yaml.load(f)['routers']
print (threads_conn (send_commands(item, show=command), item))
#print (send_commands(item, show=command))
#print (threads_conn (send_commands, item, commands))
#print (threads_conn (send_commands, item, filename))
