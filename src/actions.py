import subprocess
import sys
import os
from init import tb
import re
import time


# for better output from bash execs
def prety_b(_list):
    ansi_escape = re.compile(rb'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    # print(b''.join(_list).decode('ascii'))
    return b"```\n" + ansi_escape.sub(b'', b''.join(_list)) + b"\n```"


# action in a shell
def do(action, message, path='', lineInMessage=50, flashTime=5):
    print(int(time.time()), '[INFO] do: action=', action)
    _buffer = []
    if not path:
        path = os.getcwd()
    try:
        process = subprocess.Popen(
            action, shell=True, stdout=subprocess.PIPE,
            cwd=path, stderr=subprocess.PIPE)
        while True:
            start = time.time()
            output = process.stdout.readline()
            output += process.stderr.readline()
            if output:
                _buffer.append(output)
                print(output.decode('ascii'), end='')  # output in console
            if (len(_buffer) == lineInMessage or not output or
                    int(time.time() - start) > flashTime):
                if b''.join(_buffer).isspace():
                    tb.send_message(message.chat.id, "_",
                                    parse_mode="Markdown")
                else:
                    tb.send_message(message.chat.id,
                                    prety_b(_buffer),
                                    parse_mode="Markdown")
                _buffer = []
            else:
                pass

            sys.stdout.flush()
            sys.stderr.flush()
            if not output:
                break
    except Exception as e:
        tb.send_message(message.chat.id, e)
        raise e

def do_sh(action,message,charPerMessage=50):
    print(int(time.time()), '[INFO] do: action=', action)
    available_actions = []
    path = os.getcwd()
    tb.send_message(message.chat.id,
                    "Start processing...",
                    parse_mode="Markdown")
    available_actions = []
    with subprocess.Popen(
                            action, shell=True, stdout=subprocess.PIPE,
                            cwd=path, stderr=subprocess.PIPE,
                            bufsize = 1, universal_newlines=True) as p:
        _buffer = ''
        for line in p.stdout:
            available_actions.append(line)
            if len(_buffer) == charPerMessage:
                tb.send_message(message.chat.id, _buffer, parse_mode="Markdown")
                _buffer = ''
            else:
                _buffer += line
        tb.send_message(message.chat.id, _buffer, parse_mode="Markdown")


        tb.send_message(message.chat.id,
                            "Proccess execution stopped",
                            parse_mode="Markdown")
        return  available_actions
    # if p.returncode != 0:
    #    raise subprocess.CalledProcessError(p.returncode, p.args)


# span tags are not supported yet. but maybe :)
# so just leave it here, ok?
        # tb.send_message(message.chat.id,
        #                 ansi_to_html(_buffer),
        #                 parse_mode="HTML")
# def ansi_to_html(l):
#     text = b''.join(l).decode('ascii')
#     text = text.replace('[m', '</span>')
#     print(text)
#     COLOR_DICT = {
#         '31': [(255, 0, 0), (128, 0, 0)],
#         '32': [(0, 255, 0), (0, 128, 0)],
#         '33': [(255, 255, 0), (128, 128, 0)],
#         '34': [(0, 0, 255), (0, 0, 128)],
#         '35': [(255, 0, 255), (128, 0, 128)],
#         '36': [(0, 255, 255), (0, 128, 128)],
#     }

#     COLOR_REGEX = re.compile(
#         r'\[(?P<arg_1>\d+)(;(?P<arg_2>\d+)(;(?P<arg_3>\d+))?)?m')
#     BOLD_TEMPLATE = '<span style="color: rgb{}; font-weight: bolder">'
#     LIGHT_TEMPLATE = '<span style="color: rgb{}">'

#     def single_sub(match):
#         argsdict = match.groupdict()
#         if argsdict['arg_3'] is None:
#             if argsdict['arg_2'] is None:
#                 color, bold = argsdict['arg_1'], 0
#             else:
#                 color, bold = argsdict['arg_1'], int(argsdict['arg_2'])
#         else:
#             color, bold = argsdict['arg_2'], int(argsdict['arg_3'])

#         if bold:
#             return BOLD_TEMPLATE.format(COLOR_DICT[color][1])
#         return LIGHT_TEMPLATE.format(COLOR_DICT[color][0])

#     return COLOR_REGEX.sub(single_sub, text)
