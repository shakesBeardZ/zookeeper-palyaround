import time

from kazoo.client import KazooClient

from kazoo.client import KazooState


def main():
    zk = KazooClient(hosts='localhost:2181')

    zk.start()

    @zk.add_listener
    def my_listener(state):
        if state == KazooState.LOST:
            print("LOST")
        elif state == KazooState.SUSPENDED:
            print("SUSPENDED")
        else:
            print("Connected")

    # Creating Nodes
    # Ensure a path, create if necessary
    zk.ensure_path("/my/favorite")

    # Create a node with data
    # zk.create("/my/favorite/node", b"hello zookeeper.")
    # zk.create("/my/favorite/node/a", b"A")

    # Reading Data
    # Determine if a node exists
    if zk.exists("/my/favorite"):
        print("/my/favorite is existed")

    @zk.ChildrenWatch("/my/favorite/node")
    def watch_children(children):
        f = open("file.txt", "w")
        data, stat = zk.get("/my/favorite/node")
        print("Version: %s, data: %s" % (stat.version, data.decode("utf-8"))) 
        f.write(data.decode("utf-8"))
        f.close()
        print("Children are now: %s" % children)

    # Above function called immediately, and from then on
    # @zk.DataWatch("/my/favorite/node")
    # def watch_node(data, stat):
    #     print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

    # Print the version of a node and its data
    data, stat = zk.get("/my/favorite/node")
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

    # List the children
    children = zk.get_children("/my/favorite/node")
    print("There are %s children with names %s" % (len(children), children))

    # Updating Data
    zk.set("/my/favorite", b"some data")

    # Deleting Nodes
    # zk.delete("/my/favorite/node/a")

    # # Transactions
    # transaction = zk.transaction()
    # transaction.check('/my/favorite/node', version=-1)
    # transaction.create('/my/favorite/node/b', b"B")
    # results = transaction.commit()



    # @zk.DataWatch("/kazoo")
    # def watch_node(data, stat):
    #     if stat and data:
    #         print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
    #     else:
    #         print("deleted")

    while True:
        time.sleep(2)
        print('OK')

    zk.stop()

main()
# if __name__ == "__main__":
#     try:
#         main()

    # except Exception as ex:
    #     print("Ocurred Exception: %s" % str(ex))

    #     quit()

