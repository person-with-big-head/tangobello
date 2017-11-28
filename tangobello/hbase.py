import happybase


def init():
    conn = happybase.Connection('120.132.60.101')
    conn.open()
    return conn

connect = init()
