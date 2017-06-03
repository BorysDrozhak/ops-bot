import time
from init import tb_mem


def secure(fn):
    def wrapper(message):
        user_id = str(message.from_user.id)
        # do not proceed old messages
        if int((time.time() - message.date)) > 20:
            return
        # user should be authorized if whitelist
        if tb_mem.whitelisted_users_id:
            if user_id not in tb_mem.whitelisted_users_id:
                return
        # for some function should be sudo
        if not (tb_mem.IsAuthorised or fn.__name__ in tb_mem.InsecureFuncs):
            print("Insecure log in from " + fn.__name__ +
                  " by " + user_id)
            return
        fn(message)
    return wrapper


def secure_call(fn):
    def wrapper(message):
        user_id = str(message.from_user.id)
        # # user should be authorized if whitelist
        if tb_mem.whitelisted_users_id:
            if user_id not in tb_mem.whitelisted_users_id:
                return
        # for some function should be sudo
        if not (tb_mem.IsAuthorised or fn.__name__ in tb_mem.InsecureFuncs):
            print("Insecure log in from " + fn.__name__ +
                  " by " + user_id)
            return
        fn(message)
    return wrapper
