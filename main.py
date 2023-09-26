# concatenate multiple file into single file and mark it as merged
# author: Mr.Phat
# date : 26-09-2023
import os
import sys
from datetime import datetime

ENV_WORKSPACE = 'WORKSPACE'
ENV_OUPUT_FOLDER = 'OUPUT_FOLDER'
ENV_INPUT_FILE = 'INPUT_FILE'
ENV_SIGN = 'SIGN'

SIGN = "--RELEASED--"
BREAKLINE = "\n"
SPLIT_PROP= "="
ENV_FILE = ".merge-env"

env = {
    # ENV_WORKSPACE : '/mnt/d/test',
    ENV_INPUT_FILE : 'input.txt',
    ENV_OUPUT_FOLDER : 'RESULT'
}

def load_env():
    path_env = ENV_FILE
    if(len(sys.argv) > 1):
        argv1 = sys.argv[1]
        if(argv1 != None and len(argv1)  > 0):
            path_env = join_path(argv1, ENV_FILE)
    if exist_path(path_env):
        for line in open(path_env):
            line_arr = line.split(SPLIT_PROP)
            if len(line_arr) >= 2:
                key = line_arr[0].strip()
                value = line_arr[1].strip()
                if(len(key) > 0 and len(value) > 0):
                    env[key] = value
    print("LOADED ENV: {}".format(env))


def exist_path(path):
    return os.path.exists(path)

def mkdir(path):
    os.makedirs(path)

def join_path(path, parent):
    return os.path.join(path, parent)

def basename(path):
    return os.path.basename(path)

def get_workspace():
    workspace = None
    if ENV_WORKSPACE in env:
        workspace = env[ENV_WORKSPACE]
    if(len(sys.argv) > 1):
        argv1 = sys.argv[1]
        if(argv1 != None and len(argv1.strip()) > 0):
            workspace = argv1
    elif(workspace == None):
        workspace =  os.getcwd()
    print("WORKSPACE: {}".format(workspace))
    return workspace

def load_input(input):
    mapper = {}
    for line in open(input):
        line_arr = line.split(SPLIT_PROP)
        if len(line_arr) >= 2:
            key = line_arr[0].strip()
            value = line_arr[1].strip()
            if(len(key) > 0 and len(value) > 0):
                mapper[key] = value
    return mapper


def process_inputs(key, value, path_out):
    full_path = join_path(path_out, key)
    print("----PROCESSING: {}".format(full_path))
    if(exist_path(full_path) == False):
        output = open(full_path,'x')
    else:
        output = open(full_path, 'w').close()
    output = open(full_path,'a')
    # inputs = value.split(";")
    inputs = get_from_mapping(value)
    for idx , input in enumerate(inputs):
        if(input != None and len(input.strip()) > 0):
            input = input.strip()
            output.write("/* {index}. {input} */ {breakline}".format(index = idx+1 ,input=basename(input), breakline=BREAKLINE))
            output.writelines(process_input(input))
            output.write(BREAKLINE)
    print("----PROCESS DONE: {} {} {}".format(full_path, BREAKLINE, BREAKLINE))      

def get_from_mapping(path):
    path = join_path(get_workspace(), path)
    if(exist_path(path) == False):
        return ['']
    else:
        file = open(path,'r')
        return file.readlines()


def process_input(path):
    print("READING {} ...".format(path))
    content = ['']
    if(exist_path(path)):
        file = open(path,'r+')
        content = file.readlines()
        content = process_content(content)
        time = datetime.now()
        file.write("{breakline}{sign} {time}".format(breakline=BREAKLINE ,sign = getSign(), time = time.strftime("%m/%d/%Y, %H:%M:%S")))
    print("READ DONE {}{}".format(path, BREAKLINE))
    return content

def process_content(content):
    last_index = 0
    if(len(content)> 0):
        index = len(content) -1
        while(index >= 0):
            check = content[index]
            if(check.startswith(getSign())):
                last_index = index + 1
                index = -1
            index = index -1 
    return content[last_index:]

def getSign():
    return_value = SIGN
    if(ENV_SIGN in env):
        sign_value = env[ENV_SIGN]
        if(sign_value != None and len(sign_value) > 0):
            return_value = sign_value
    return return_value

if __name__ == '__main__':
    load_env()
    output = env[ENV_OUPUT_FOLDER]
    workspace = get_workspace()
    full_path = join_path(workspace, output)
    input_path = join_path(workspace, env[ENV_INPUT_FILE])
    input_mapper = load_input(input_path)
    if(exist_path(full_path) == False): 
        mkdir(full_path)
    for k,v in input_mapper.items():
        process_inputs(k,v, full_path)
    print("DONE!")