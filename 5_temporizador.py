from paho.mqtt.client import Client

from time import sleep
from random import randint,random


def main(broker):
    client = Client()

    client.connect(broker)
    client.loop_start()
    
    print('Publishing')

    while True:
        t = randint(0,8)
        data= f'[espera:{t},topic: /clients/{t},message: hello to {t}]'    
        client.publish('/clients/tiempo',  data)
        print('.', end= '', flush=True)
        sleep(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        print(f"Usage: {sys.argv[0]}")
    broker = sys.argv[1]
    main(broker)