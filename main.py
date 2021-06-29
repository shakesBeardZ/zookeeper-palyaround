import glob
import asyncio
from kazoo.client import KazooClient, KazooState
from kazoo.exceptions import LockTimeout
from kazoo.exceptions import NodeExistsError
from kazoo.exceptions import NoNodeError
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


async def init() -> None:
    pass
    for filename in glob.iglob("templates" + '**/**/**/**.yml', recursive=True):
        # print("pushing {} to zookeeper".format(filename))
        f = open(filename, "r")
        # print(f.read())
        # try:
        if zk.exists("/" + filename):
            print(filename + "node already exists")
            zk.set("/" + filename,  bytes(f.read(), 'utf-8'))
        else:
            print(filename + "node don't exists")
            zk.ensure_path("/" + filename)
            zk.set("/" + filename,  bytes(f.read(), 'utf-8'))
        # except NoNodeError as e:
        #     logger.info(e)


async def main() -> None:
    print("Creating initial data")
    await init()
    print("Initial data created")

if __name__ == "__main__":
    asyncio.run(main())


