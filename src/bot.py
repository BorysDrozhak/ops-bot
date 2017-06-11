import os
from init import tb, tb_mem  # init telebot and config obj
from wrappers import secure, secure_call  # place for wrappers
from markups import Main_insec, Main_sec
from markups import g_markup, g_inl_mark
from actions import *  # place for actions


def markdown(text):
    return '```\n' + str(text) + '\n```'


@tb.message_handler(commands=['help', 'start', 'hi', 'hello'])
@secure
def send_welcome(message):
    text = "Howdy, how are you doing?"
    list_handlers = [item['filters']['commands']
                     for item in tb.message_handlers
                     if isinstance(item['filters']['commands'], list)]
    handlers = ''
    for l in list_handlers:
        for i, item in enumerate(l):
            handlers += "/" + item + '\t\t'
            if i == 0:
                handlers += '\t\t'
        handlers += '\n'

    tb.send_message(message.chat.id, text, reply_markup=Main_insec)
    if tb_mem.IsAuthorised:
        tb.send_message(message.chat.id,
                        "<b>here is what we can:</b>\n" +
                        str(handlers), reply_markup=Main_sec,
                        parse_mode="HTML")


@tb.message_handler(commands=['sudo'])
@secure
def sudo(message):
    if len(message.text.split()) > 1:
        if message.text.split()[1] == tb_mem.secretQuestion:
            tb_mem.IsAuthorised = True
            tb.send_message(message.chat.id, 'Hello ' +
                            str(message.from_user.id), reply_markup=Main_sec)
    else:
        print(str(message.from_user.id) + " is trying sudo")


@tb.message_handler(commands=['make'])
@secure
def make_handle(message):
    command = """make -qp $makef $makef_dir 2>/dev/null |
awk -F':' '/^[a-zA-Z0-9][^$#\/\t=]*:([^=]|$)/ \
{split($1,A,/ /);for(i in A)print A[i]}'
"""
    # Execute command and get list of lines as output
    L = (do_sh(command, message))
    # Generate inline with needed prefix
    m = g_inl_mark(L, message.text.split()[0])
    tb.send_message(message.chat.id, '.' * 50, reply_markup=m)


@tb.callback_query_handler(func=lambda call: '/make' in call.data)
@secure_call
def call_make(call):
    print(do_sh(call.data[1:]))


@tb.message_handler(commands=['ls'])
@secure
def ls(message):
    files = [f for f in os.listdir(os.getcwd())]
    mark = g_inl_mark(files, prefix='/ls')
    tb.send_message(message.chat.id,
                    '-', reply_markup=mark)

    response = '<strong>your dir:</strong>\n' + '\n'.join(files)
    m = g_markup(['/projects'] + files)
    tb.send_message(message.chat.id,
                    response, parse_mode="HTML",
                    reply_markup=m)
    # like in bash after [1:]
    action = "ls -la"
    for path in message.text.split()[1:]:
        do(action, message, path=path)


@tb.message_handler(func=lambda m: len(m.text.split()) == 1)
@secure
def cat(message):
    replay = "cat file " + message.text
    try:
        with open(message.text) as file:
            content = file.read()
    except Exception as e:
        content = str(e)
    try:
        tb.send_message(message.chat.id, replay + '\n' + markdown(content),
                        parse_mode='Markdown', reply_markup=Actions)
    except Exception as e:
        tb.send_message(message.chat.id, markdown(e), parse_mode='Markdown')


if __name__ == '__main__':
    tb.polling(none_stop=True, timeout=50)
