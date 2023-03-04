
import time
import websocket #upm package(websocket-client)
import json
import threading
import requests
import sys
from websocket._exceptions import WebSocketConnectionClosedException #upm package(websocket-client)



sys.setrecursionlimit(10**9)
token = "token"
message = "Stop sending your retard messages: \"|\"  Also if u send : more messages/call, i will auto-block you!"
call_message = "Stop calling moron! (btw i have auto call ending so i dont even hear you ringing! Also if u send : more messages/call, i will auto-block you!)"
img_message = "Nice image dude (\"|\"). But if u send : more messages/call, i will auto-block you!"
while True:
    try:
        print(requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"authorization": token}, json={"status": "online"}))
        break
    except:
        continue

def send_json_request(ws, request):
    ws.send(json.dumps(request))
def receive_json_response(ws):
    try:
        
        response = ws.recv()
    except WebSocketConnectionClosedException as e:
        receive_json_response(ws)
    if response:
        return json.loads(response)


def heartbeat(interval, ws):
    print("Heartbeat begin")
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        #print("heartbeat sent")

ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?encoding=json&v=9")
event = receive_json_response(ws)
print(event)

heartbeat_interval = event["d"]["heartbeat_interval"] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))


payload = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": "android",
                    "$browser": "Discord Android",
                    "$device": "discord.js"
                }
            }
        }
send_json_request(ws, payload)
running = True
dankbot = False
rainbow_mode_active = False
spammers = []


while True:
    try:
        event = receive_json_response(ws)
    except:
        continue
    
    try:
        if event["d"]["author"]:
        
            username = event["d"]["author"]["username"]
            content = event["d"]["content"]
            channelid = event["d"]["channel_id"]
            try:
                guild = event["d"]["author"]["guild_id"]
            except:
                pass
            try:
                msgid = event["d"]["id"]
            except:
                pass
            with open("convos.txt", "r") as file: convos = file.read()
            with open("block_amount.txt", "r") as file: block_amount = file.read()
            #with open("blocked.txt", "r") as file: blocked = file.read().split("\n")
            if channelid in convos.split("\n") and event["d"]["author"]["id"] != "656519115992858624":
                    
                with open("running.txt", "r") as file: running = file.read()
                
                if running == "True":
                    user_in_spammers = False
                    
                    for i in range(len(spammers)):
                        if event["d"]["author"]["id"] in spammers[i]:
                            spammers[i][1] += 1
                            number_of_messages = spammers[i][1]
                            user_in_spammers = True
                            
                            if number_of_messages >= int(block_amount):
                                userid = event["d"]["author"]["id"]
                                #blocked.append(userid)
                                #with open("blocked.txt", "a") as file: file.write(id + "\n")
                                
                                r = requests.put(f"https://discord.com/api/v9/users/@me/relationships/{userid}", json={"type": "2"}, headers={"authorization": token, "content-type": "application/json"})
                                print(r, r.text)
                                spammers.pop(i)
                    if not user_in_spammers:
                        list_maker = [event["d"]["author"]["id"], 1]
                        spammers.append(list_maker)
                        number_of_messages = 1
                            
                    print(spammers)
                    try:
                        if event["d"]["call"]:
                            time.sleep(1)
                            r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/call/stop-ringing", headers={"authorization": token, "content-type": "application/json"}, json={})
                            r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", json={"content": call_message.replace(":", str(int(block_amount) - number_of_messages))}, headers={"authorization": token})
                            print(r.text, r)
                        
                    except KeyError as e:
                            if event["d"]["attachments"]:
                                #print("sent no (image)")
                                #print(event["d"]["attachments"])
                                r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", json={"content": img_message.replace("|", event["d"]["attachments"][0]["filename"]).replace("-", event["d"]["attachments"][0]["url"]).replace(":", str(int(block_amount) - number_of_messages)), "message_reference": {"channel_id": channelid, "message_id": msgid}, "tts": "true"}, headers={"authorization": token})
                                #print(r.text, r)
                            else:
                                try:
                                    #print(e)
                                    print(event)
                                    print("sent no")
                                    r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", json={"content": message.replace("|", content).replace(":", str(int(block_amount) - number_of_messages)), "message_reference": {"channel_id": channelid, "message_id": msgid}, "tts": "true"}, headers={"authorization": token})
                                    #print(r.text, r)
                                except:
                                    #print(e)
                                    pass
                            #print(e)
            elif "dream" in content.lower() and event["d"]["author"]["id"] != "656519115992858624":
                print(event["d"]["author"]["id"])
                r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", json={"content": "Dream is trash lol, get a life and unsub", "message_reference": {"channel_id": channelid, "message_id": msgid}}, headers={"authorization": token})
                print(r, r.text)
                        
            elif event["d"]["author"]["id"] in ("782301802367287308", "656519115992858624") :
                if content.startswith("!running"):
                    with open("running.txt", "r") as file: running = file.read()
                    if running == "True":
                        running = False
                    else:
                        running = True
                    with open("running.txt", "w") as file: file.write(str(running))
                    r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", data={"content": f"Succesfully changed the status to: {str(running)}"}, headers={"authorization": token})

                
                
                elif content.startswith("!dankbot"):
                    dankbot = not dankbot
                    r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", data={"content": f"Succesfully changed the status to: {str(dankbot)}"}, headers={"authorization": token})
                elif content.startswith("!message"):
                    message = content.replace("!message", "")
                    r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", data={"content": f"Succesfully changed the message to: {str(message)}"}, headers={"authorization": token})
                elif content.startswith("!call_message"):
                    call_message = content.replace("!call_message", "")
                    r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", data={"content": f"Succesfully changed the call message to: {str(message)}"}, headers={"authorization": token})
                elif content.startswith("!img_message"):
                    img_message = content.replace("!img_message", "")
                    r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", data={"content": f"Succesfully changed the image message to: {str(message)}"}, headers={"authorization": token})
                elif content.startswith("!convoadd"):
                    with open("convos.txt", "a") as file: file.write(str(event["d"]["channel_id"]) + "\n")
                    
                    r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", data={"content": f"Added this person to the bot!"}, headers={"authorization": token})
                elif content.startswith("!convorem"):
                    
                    with open("convos.txt", "r") as file: filecontent = file.read()
                    with open("convos.txt", "w") as file: file.write(filecontent.replace(str(event["d"]["channel_id"]) + "\n", ""))
                    
                    r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", data={"content": f"Removed from the bot"}, headers={"authorization": token})
                elif content.startswith("!unblock"):
                    with open("blocked.txt", "r") as file: filecontent = file.read()
                    with open("blocked.txt", "w") as file: file.write(filecontent.replace(str("", "")))
                elif content.startswith("!block_amount"):
                    content = content.replace("!block_amount ", "")
                    with open("block_amount.txt", "r") as file: filecontent = file.read()
                    with open("block_amount.txt", "w") as file: file.write(content)
                    r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", data={"content": f"Block amount is now {content}"}, headers={"authorization": token})
                
                elif content.startswith("!block"):
                        try:
                            if content.split(" ")[1]:
                                userid = content.replace("!block")
                            else:
                                userid = False
                        except:
                            pass
                        
                        if userid:
                            print(requests.put(f"https://discord.com/api/v9/users/@me/relationships/{userid}", json={"type": "2"}, headers={"authorization": token}).text)
                        else:
                            blocked.append(event["d"]["channel_id"])
                            with open("blocked.txt", "a") as file: file.write(str(userid) + "\n")
                        r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", data={"content": f"Gonna block them next time they send a message! (or blocked them already if u provided an id!)"}, headers={"authorization": token})
                        with open("convos.txt", "r") as file: filecontent = file.read()
                        with open("convos.txt", "w") as file: file.write(filecontent.replace(str(event["d"]["channel_id"]), ""))
                elif content.startswith("!unblock"):
                    try:
                        if content.split(" ")[1]:
                            userid = content.replace("!unblock")
                        else:
                            userid = False
                    except:
                        pass
                    blocked.remove(userid)
                    with open("blocked.txt", "r") as file: filecontent = file.read()
                    with open("blocked.txt", "w") as file: file.write(filecontent.replace(str(userid), ""))
                    if userid:
                        r = requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{userid}", headers={"authorization": token})
                    r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", data={"content": f"Succesfully unblocked"}, headers={"authorization": token})
                    with open("convos.txt", "a") as file: file.write(str(event["d"]["channel_id"]) + "\n")

                
            if content.startswith("!status"):
                content = content.split(" ")[1]
                print(requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"authorization": token}, json={"status": content}))
                r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", data={"content": f"Succesfully changed the status to: {content}"}, headers={"authorization": token})
            
            elif content.startswith("!rainbow"):
                if not rainbow_mode_active:
                    try:
                        r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", data={"content": f"Rainbow mode activated!"}, headers={"authorization": token})
                        rainbow_mode_active = True
                        def rainbow_mode(none=None):
                            global rainbow_mode_active
                            for i in range(100):
                                for term in ("online", "dnd", "idle", "invisible"):
                                    if rainbow_mode_active:
                                        print(requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"authorization": token}, json={"status": term}))
                                        time.sleep(0)
                        threading._start_new_thread(rainbow_mode, (None,))
                    except Exception as e:
                        #print(e)
                        pass
                        
                else:
                    r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", data={"content": f"Rainbow mode is already active!"}, headers={"authorization": token})
            elif content.startswith("!rainbow off"):
                rainbow_mode_active = False
            elif content.startswith("I will suck your cock"):
                with open("convos.txt", "r") as file: filecontent = file.read()
                with open("convos.txt", "w") as file: file.write(filecontent.replace(str(event["d"]["channel_id"]) + "\n", ""))
                
                r = requests.post(f"https://discord.com/api/v9/channels/{channelid}/messages", data={"content": f"Removed from the bot"}, headers={"authorization": token})
            elif "event" in content and username == "Dank Memer":
                if dankbot:
                    cid = event["d"]["components"][0]["components"][0]["custom_id"]
                    payload = {
                                "data": {
                                    "component_type": 2,
                                    "custom_id": cid},
                                "channel_id": channelid,
                                "guild_id": guild,
                                "message_id": msgid,
                                "application_id": "270904126974590976",
                                "type": 3
                                }
                    r = requests.post(
                                "https://discord.com/api/v9/interactions",
                                headers={"authorization": token},
                                json=payload)
                    print(r.text)
            op_code = event["op"]
            if op_code == 11:
                print(event)
                print("heartbeat received")
            
            #print(event)            
            
            
    except Exception as e:
        print(e)
        pass
    op_code = event["op"]
    if op_code == 1:
        print(event)
        print("heartbeat received")
            
