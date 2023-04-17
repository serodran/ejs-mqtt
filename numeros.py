from paho.mqtt.client import Client
import traceback
import sys
from sympy import isprime


def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    try:
        n = float(msg.payload)
        if n // 1 == 0.0:
            client.publish('/clients/reales',msg.payload)
            userdata['frecuencia']['reales'] += 1
            client.publish('/clients/frecreales', f'{userdata["frecuencia"]["reales"]}')
        else:
            n = int(msg.payload)
            primo = isprime(int(n))
            client.publish('/clients/enteros',f'{msg.payload} es primo: {primo}')
            userdata['frecuencia']['enteros'] += 1
            client.publish('/clients/frecenteros', f'{userdata["frecuencia"]["enteros"]}')
            userdata['suma']['suma'] += n
            client.publish('/clients/suma', f'{userdata["suma"]["suma"]}')
            if n % 2 == 0:
                client.publish('/clients/par', msg.payload)
            else:
                client.publish('/clients/impar', msg.payload)
            
        
    except ValueError:
        pass
    except Exception as e:
        raise e


def main(broker):
    userdata = {'suma' : {'suma':0},
                'frecuencia' :{'enteros':0,'reales':0}}
    client = Client(userdata=userdata)
    client.on_message = on_message

    print(f'Connecting on channels numbers on {broker}')
    client.connect(broker)

    client.subscribe('numbers')

    client.loop_forever()


if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)
