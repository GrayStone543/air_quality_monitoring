import requests
import json


def upload_data(GAS_URL, v1, v2):
    # 準備要傳送的資料格式 (對應 GAS 裡的 data.value1, data.value2 )
    payload = { "value1": v1, "value2": v2 }

    try:
        response = requests.post(GAS_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            print(f"Send to remote success! Response: {response.text}")
        else:
            print(f"Failed! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    with open("url.txt", "rt") as f:
        GAS_URL = f.readline()
        GAS_URL = GAS_URL.rstrip()
    print(f"type: {type(GAS_URL)} {GAS_URL}")
    
    test_temp = 17.1
    test_humi = 50.5

    upload_data(GAS_URL, test_temp, test_humi)
    
