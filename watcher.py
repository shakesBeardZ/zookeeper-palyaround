import time
from kazoo.client import KazooClient, KazooState
from logs import log_conf

logger = log_conf.Logger(__name__)
zk = KazooClient(hosts="localhost:2181")


def zk_listener(state):
    if state == KazooState.LOST:
        print("Connection to ZooKeeper LOST")
        pass
    elif state == KazooState.SUSPENDED:
        print("Connection to ZooKeeper SUSPENDED")
        pass
    else:
        print("Connection to ZooKeeper Recieved")


zk.add_listener(zk_listener)
zk.start()

sms_ar_childern = zk.get_children("/templates/sms/ar/",)
sms_en_childern = zk.get_children("/templates/sms/en/",)
# pn_childern = zk.get_children("/templates/push_notification/",)
# email_childern = zk.get_children("/templates/",)

for child in sms_ar_childern:
    children_testing = zk.get_children("/templates/sms/ar/send_gift.yml/")
    if children_testing != []:
        @zk.ChildrenWatch("/templates/sms/ar/send_gift.yml")
        def watch_children(children):
            print(children)
    else:
        @zk.ChildrenWatch("/templates/sms/ar/")
        def watch_children(children):
            print(children)

for child in sms_en_childern:
    children_testing = zk.get_children("/templates/sms/ar/send_gift.yml/")
    if children_testing != []:
        @zk.ChildrenWatch("/templates/sms/ar/send_gift.yml")
        def watch_children(children):
            print(children)
    else:
        @zk.ChildrenWatch("/templates/sms/ar/")
        def watch_children(children):
            print(children)
