import requests

r = requests.post("https://discord.com/api/v9/channels/826129057846132766/call/ring", headers={"authorization": "NzgyMzAxODAyMzY3Mjg3MzA4.Yg641A.Zu7MmAhaMxNhlCI5vQP3YCdT4Qc", "content-type": "application/json"}, json={})
print(r, r.text)