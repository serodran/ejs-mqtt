from paho.mqtt.client import Client
import traceback
import sys
import time


def datos(userdata):
    t = userdata["t"]
    m = min(t)
    M = max(t)
    med = sum(t) // len(t)
    
    t1 = userdata["t1"]
    m1 = min(t1)
    M1 = max(t1)
    med1 = sum(t1) // len(t1)
    
    t2 = userdata["t2"]
    m2 = min(t2)
    M2 = max(t2)
    med2 = sum(t2) // len(t2)
    
    print(f'Total- max: {M}, min: {m}, media: {med}')
    print(f't1- max: {M1}, min: {m1}, media: {med1}')
    print(f't2- max: {M2}, min: {m2}, media: {med2}')

    
    
def on_message(client, userdata, msg):

    try:
        print(msg.topic, msg.payload)
        n =  float(msg.payload)
        userdata["t"].append(n)
        
        if msg.topic == 'temperature/t1':
            userdata["t1"].append(n)
        else:
            userdata["t2"].append(n)
            
        #client.publish('/clients/tempMar',f'media: {userdata}')
        #med = userdata["suma"]//len(temps)
        #client.publish('/clients/temps',med)
    except ValueError:
        pass
    except Exception as e:
        raise e


def main(broker):
    userdata = {'t':[], 't1':[],'t2':[]}
    client = Client(userdata=userdata)
    client.on_message = on_message

    print(f'Connecting on channels temperature on {broker}')
    client.connect(broker)
    
    client.subscribe('temperature/#')

    client.loop_start()
    
    while True:
        time.sleep(6)
        datos(userdata)


if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)