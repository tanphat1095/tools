# concatenate multiple file into single file and mark it as merged
# author: Mr.Phat
# date : 26-09-2023
import os
from datetime import datetime
import argparse
from GitHelper import GitHelper
import pathlib
from pathlib import Path

ENV_WORKSPACE = 'WORKSPACE'
ENV_OUPUT_FOLDER = 'OUPUT_FOLDER'
ENV_INPUT_FILE = 'INPUT_FILE'
ENV_SIGN = 'SIGN'
ENV_GET_ALL="GET_ALL"
ENV_CREATE_NEW_SUB = "CREATE_NEW_SUB"
ENV_FOLDER_TIME_FORMAT="FOLDER_TIME_FORMAT"
ENV_GIT_REPO = "GIT_REPO"
ENV_CONCAT_CHAR="CONCAT_CHAR"
ENV_WHITE_LIST = "WHITE_LIST"

SIGN = "--RELEASED--"
BREAKLINE = "\n"
SPLIT_PROP= "="
ENV_FILE = ".merge-env"
SPLIT_MULTI_VALUE = ";"

env = {
    # ENV_WORKSPACE : '/mnt/d/test',
    ENV_INPUT_FILE : 'input.txt',
    ENV_OUPUT_FOLDER : 'RESULT',
    ENV_FOLDER_TIME_FORMAT: '%Y%m%d_%H%M%S',
    ENV_CREATE_NEW_SUB : 'False',
    ENV_CONCAT_CHAR : 'GO',
    ENV_WHITE_LIST: '.sql;.java;.txt'


}

def load_env(args):
    path_env = ENV_FILE
    if args.workspace is not None:
        path_env = join_path(args.workspace, ENV_FILE)
    if exist_path(path_env):
        for line in open(path_env):
            line_arr = line.split(SPLIT_PROP)
            if len(line_arr) >= 2:
                key = line_arr[0].strip()
                value = line_arr[1].strip()
                if(len(key) > 0 and len(value) > 0):
                    env[key] = value
    load_env_args(args)
    # print("LOADED ENV: {}".format(env))


def exist_path(path):
    return os.path.exists(path)

def mkdir(path):
    os.makedirs(path)

def join_path(*dirs):
    # return os.path.join(path, parent)
    return Path(*dirs)

def basename(path):
    return os.path.basename(path)

def isfile(path):
    return os.path.isfile(path)

def lstdir(path):
    return os.listdir(path)

def get_all_file(path):
    result = []
    for dir in lstdir(path):
        dir = join_path(path, dir)
        if(isfile(dir) == True):
            result.append(dir)

    return result

def get_workspace():
    workspace = None
    if ENV_WORKSPACE in env:
        workspace = env[ENV_WORKSPACE]
    work = parse_args().workspace
    if(work is not None):
        workspace = work
    elif(workspace == None):
        workspace =  os.getcwd()
    print("WORKSPACE: {}".format(workspace))
    return workspace

def load_input(input):
    mapper = {}
    if exist_path(input):
        for line in open(input):
            line_arr = line.split(SPLIT_PROP)
            if len(line_arr) >= 2:
                key = line_arr[0].strip()
                value = line_arr[1].strip()
                if(len(key) > 0 and len(value) > 0):
                    mapper[key] = value
    else:
        print("Cannot find mapping file with 'ENV_INPUT_FILE' config in .merge-env in workspace")
    return mapper


def process_inputs(key, value, path_out):
    full_path = join_path(path_out, key)
    get_all: bool = False
    if(ENV_GET_ALL in env):
        get_all_values = env[ENV_GET_ALL].split(SPLIT_MULTI_VALUE)
        get_all = key in get_all_values

    print("----PROCESSING: {}".format(full_path))
    if(exist_path(full_path) == False):
        output = open(full_path,'x')
    else:
        output = open(full_path, 'w').close()
    output = open(full_path,'a', encoding="utf8")
    # inputs = value.split(";")
    inputs = get_from_mapping(value)
    for idx , input in enumerate(inputs):
        if(input != None and len(input.strip()) > 0) and check_extension(input):
            input = input.strip()
            output.write("/* {index}. {input} */ {breakline}".format(index = idx+1 ,input=basename(input), breakline=BREAKLINE))
            output.writelines(process_input(input, get_all))
            output.write(BREAKLINE)
            if ENV_CONCAT_CHAR in env:
                output.write(env[ENV_CONCAT_CHAR])
    if(output.closed == False):
        output.close()
    print("----PROCESS DONE: {} {} {}".format(full_path, BREAKLINE, BREAKLINE))      
def check_extension(filename):
    whitelist = env[ENV_WHITE_LIST].strip().split(SPLIT_MULTI_VALUE)
    extension = pathlib.Path(filename).suffix
    return extension in whitelist

def get_from_mapping(path):
    path = join_path(get_workspace(), path)
    if(exist_path(path) == False):
        return ['']
    else:
        return get_all_input(path)

def write_concat():
    if ENV_CONCAT_CHAR in env and env[ENV_CONCAT_CHAR] is not None and len(env[ENV_CONCAT_CHAR]):
        return env[ENV_CONCAT_CHAR]

def get_all_input(path):
    result = None
    if(isfile(path) == True):
        file = open(path,'r')
        result = file.readlines()
        if(file.closed == False):
            file.close()
    else:
        result = get_all_file(path)
    return result

def process_input(path, get_all = False):
    print("READING {} ...".format(path))
    content = ['']
    if(exist_path(path)):
        file = open(path,'r+', encoding="utf8")
        content = file.readlines()
        if(get_all == False):
            content = process_content(content)
            time = datetime.now()
            file.write("{breakline}{sign} {time}".format(breakline=BREAKLINE ,sign = getSign(), time = time.strftime("%m/%d/%Y, %H:%M:%S")))
        if(file.closed == False):
            file.close()
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

def check_create_subrirect():
    result = False
    if ENV_CREATE_NEW_SUB in env:
        create_new_sub = env[ENV_CREATE_NEW_SUB]
        result = create_new_sub != None and create_new_sub.lower() == 'true'
    return result

def format_sub_direct():
    time_format = env[ENV_FOLDER_TIME_FORMAT]
    return datetime.now().strftime(time_format)

def check_commit(args):
    if ENV_GIT_REPO in env:
        repo = env[ENV_GIT_REPO]
        helper = GitHelper(repo)
        files = []
        for file in helper.get_by_commit(args.check_commit):
            print(file)
            files.append(file)
        if args.output is not None:
            write_out(files, args.output)
    else:
        print('Please specify git repo with --git-repo argument or GIT_REPO value in .merge-env file')

def write_out(data, output):
    file = open(output, 'w')
    for line in data:
        file.write("{line}{breakline}".format(line = line, breakline = BREAKLINE))

def main_function():
    args = parse_args()
    load_env(args)
    if args.check_commit is not None:
        check_commit(args)
    if args.merge == True:
        output = env[ENV_OUPUT_FOLDER]
        workspace = get_workspace()
        if workspace is None:
            print('Cannot find workspace')
        full_path = join_path(workspace, output)
        if(check_create_subrirect() == True):
            full_path = join_path(full_path, format_sub_direct())
        input_path = join_path(workspace, env[ENV_INPUT_FILE])
        input_mapper = load_input(input_path)
        if(exist_path(full_path) == False and len(input_mapper.items()) > 0): 
            mkdir(full_path)
        for k,v in input_mapper.items():
            process_inputs(k,v, full_path)
    print("DONE!")

def parse_args():
    parser = argparse.ArgumentParser("merge-file")
    parser.add_argument('--git-repo', help='specify the git repository', type=str)
    parser.add_argument('--workspace', help='Specify the workspace', type=str)
    parser.add_argument('--check-commit', help='Get all file from commit split by ","', type=str)
    parser.add_argument('--merge', help='Start merge file', action='store_true')
    parser.add_argument('-o', '--output', help='Write to output file', type=str)
    return parser.parse_args()

def load_env_args(args):
    if args.git_repo is not None:
        env[ENV_GIT_REPO] = args.git_repo
    if args.workspace is not None:
        env[ENV_WORKSPACE] = args.workspace

if __name__ == '__main__':
    main_function()