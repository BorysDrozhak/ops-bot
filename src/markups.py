from telebot import types


def g_markup(L):
    markup = types.ReplyKeyboardMarkup()
    markup.add(*[types.KeyboardButton(b) for b in L])
    return markup


def g_inl_mark(L, prefix=''):
    # prefix is needed when you want call back with commands like:
    # /ls inline-name
    if prefix:
        prefix += ' '
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 10
    for el in L:
        markup.add(types.InlineKeyboardButton(text=str(el),
                                              callback_data=str(
            prefix + el),
            switch_inline_query=str(prefix + el)))
    return markup


# buttons
p = '/projects'  # shows projs
projs = ['/epicEel', '/telebot', '/Kafka']
ls = '/ls'
test = '/test'
actions = ['/make', ls, '/git']
env = ['/dev', '/stage', '/prod']

# keyboards
Environments = g_markup(env + [p])
Actions = g_markup(actions + [p])
Main_sec = g_markup([p, ls, test])
Test = g_markup(actions + [p])
Main_insec = g_markup(['/start', '/sudo', test])
Projects = g_markup(projs + [test])
