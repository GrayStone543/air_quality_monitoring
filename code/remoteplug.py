import asyncio
import os
from tapo import ApiClient, DiscoveryResult
import json
import sys


async def tapo_find_dev(dev_info:dict):
    tapo_username = dev_info["username"]
    tapo_password = dev_info["password"]
    target = dev_info["ip address"]
    api_client = ApiClient(tapo_username, tapo_password)
    timeout_s = 10
    discovery = await api_client.discover_devices(target, timeout_s)

    async for discovery_result in discovery:
        try:
            device = discovery_result.get()

            match device:
                case DiscoveryResult.GenericDevice(device_info, _handler):
                    print(
                        f"Found Unsupported Device '{device_info.nickname}' of model '{device_info.model}' at IP address '{device_info.ip}'."
                    )
                case DiscoveryResult.Light(device_info, _handler):
                    print(
                        f"Found '{device_info.nickname}' of model '{device_info.model}' at IP address '{device_info.ip}'."
                    )
                case DiscoveryResult.ColorLight(device_info, _handler):
                    print(
                        f"Found '{device_info.nickname}' of model '{device_info.model}' at IP address '{device_info.ip}'."
                    )
                case DiscoveryResult.RgbLightStrip(device_info, _handler):
                    print(
                        f"Found '{device_info.nickname}' of model '{device_info.model}' at IP address '{device_info.ip}'."
                    )
                case DiscoveryResult.RgbicLightStrip(device_info, _handler):
                    print(
                        f"Found '{device_info.nickname}' of model '{device_info.model}' at IP address '{device_info.ip}'."
                    )
                case DiscoveryResult.Plug(device_info, _handler):
                    print(
                        f"Found '{device_info.nickname}' of model '{device_info.model}' at IP address '{device_info.ip}'."
                    )
                case DiscoveryResult.PlugEnergyMonitoring(device_info, _handler):
                    print(
                        f"Found '{device_info.nickname}' of model '{device_info.model}' at IP address '{device_info.ip}'."
                    )
                case DiscoveryResult.PowerStrip(device_info, _handler):
                    print(
                        f"Found Power Strip of model '{device_info.model}' at IP address '{device_info.ip}'."
                    )
                case DiscoveryResult.PowerStripEnergyMonitoring(device_info, _handler):
                    print(
                        f"Found Power Strip with Energy Monitoring of model '{device_info.model}' at IP address '{device_info.ip}'."
                    )
                case DiscoveryResult.Hub(device_info, _handler):
                    print(
                        f"Found '{device_info.nickname}' of model '{device_info.model}' at IP address '{device_info.ip}'."
                    )
        except Exception as e:
            print(f"Error discovering device: {e}")

async def p105_ctrl(dev_info:dict, turn_on=False):
    tapo_username = dev_info["username"]
    tapo_password = dev_info["password"]
    ip_address = dev_info["ip address"]
    client = ApiClient(tapo_username, tapo_password)
    device = await client.p105(ip_address)

    if turn_on:    
        print("Turning device on...")
        await device.on()
    else:        
        #print("Waiting 2 seconds...")
        #await asyncio.sleep(2)
        print("Turning device off...")
        await device.off()

    #device_info = await device.get_device_info()
    #print(f"Device info: {device_info.to_dict()}")


if __name__ == "__main__":
    cwd = os.path.dirname(os.path.abspath(sys.argv[0]))
    INFO_FILE = os.path.join(cwd, "device_info.json")
    if os.path.exists(INFO_FILE):
        with open(INFO_FILE, "r") as f:
            dev_info = json.load(f)
        asyncio.run(p105_ctrl(dev_info, False))
        #asyncio.run(tapo_find_dev(dev_info))
    else:
        print("No device information!")
