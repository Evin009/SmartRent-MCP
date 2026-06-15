import asyncio
import os
import smartrent
from dotenv import load_dotenv

load_dotenv()


async def main():
    print("Connecting to SmartRent")
    api = await smartrent.async_login(os.getenv("SMARTRENT_EMAIL"),
                                      os.getenv("SMARTRENT_PASSWORD"))
    print("Connected")
    
    locks = api.get_locks()
    thermostat = api.get_thermostats()
    switches = api.get_binary_switches()
    sensors = api.get_leak_sensors()
    
    # print(f"Locks : {len(locks)}")
    # print(f"Thermosats : {len(thermostat)}")
    # print(f"Switches : {len(switches)}")
    # print(f"Sensors : {len(sensors)}")
    
    # testing switch controls and listing names of devices
    switch_names = [s.get_name() for s in switches]
    print(switch_names)
    
    
asyncio.run(main())
