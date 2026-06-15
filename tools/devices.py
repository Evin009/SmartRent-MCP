import os
import smartrent
from dotenv import load_dotenv

load_dotenv()

# make the api call
async def get_api():
    return await smartrent.async_login(os.getenv("SMARTRENT_EMAIL"),
                                      os.getenv("SMARTRENT_PASSWORD"))

# fetch device status
async def fetch_devices_status() -> str:
    api = await get_api()
    
    results = []
    
    for lock in api.get_locks():
        results.append(f"Lock '{lock.get_name()}' : {'Locked' if lock.get_locked() else 'Unlocked'}")
        
    for therm in api.get_thermostats():
        results.append(f"Thermostat '{therm.get_name()}': {therm.get_current_temp()}°F, set to {therm.get_cooling_setpoint()}°F")
    
    for switch in api.get_switches():
        results.append(f"Switch '{switch.get_name()}': {'On' if switch.get_on() else 'Off'}")
    
    for sensor in api.get_leak_sensors():
        results.append(f"Sensor '{sensor.get_name()}': {'Leak detected!' if sensor.get_active() else 'Dry'}")
    
    return "\n".join(results)


# adding switch control
async def control_switch(name: str, action: str) -> str:
    """Turns a switch on or off by name"""
    api = await get_api()
    switches = api.get_switches()
    
    for switch in switches:
        if name.lower() in switch.get_name().lower():
            if action == 'on':
                await switch.async_set_on(True) # setting switch on
            elif action == 'off':
                await switch.async_set_on(False) # setting switch off
            else:
                return f"Unknown action '{action}'. Use 'on' or 'off'."
            return f"{switch.get_name()} turned {action}"
    
    return f"No switch found matching '{name}'. Available: {[s.get_name() for s in switches]}"


# adding front door lock control
async def control_lock(action: str) -> str:
    """Lock or unlcok the front door"""
    api = await get_api()
    locks = api.get_locks()
    
    if not locks:
        return "No locks found on this account"
    
    lock = locks[0]
    
    if action == 'lock':
        await lock.async_set_locked(True)
        return f"{lock.get_name()} is now locked"
    elif action == 'unlock':
        await lock.async_set_locked(False)
        return f"{lock.get_name()} is now unlocked"
    else:
        return f"Unknown action '{action}'. Use 'lock' or 'unlock'."
    
    
async def control_temperature(temperature: int, mode: str = "cool", unit: str = "F") -> str:
    """Set the thermostat temperature and mode"""
    
    api = await get_api()
    thermostats = api.get_thermostats()
    
    if not thermostats:
        return f"No thermostat found on this account"
    
    # convert C to F if needed
    if unit.upper()  == 'C':
        temperature = int((temperature * 9/5) + 32)
        
    therm = thermostats[0]
    
    
    accepted_modes = ['cool', 'heat', 'auto', 'off']
    
    if mode not in accepted_modes:
        return f"Invalid mode {mode}. Use one of: {accepted_modes}"

    if mode == 'cool':
        await therm.async_set_cooling_setpoint(temperature)
    elif mode == 'heat':
        await therm.async_set_heating_setpoint(temperature)
    elif mode == 'auto':
        await therm.async_set_cooling_setpoint(temperature)
        await therm.async_set_heating_setpoint(temperature)
    elif mode == 'off':
        await therm.async_set_mode('off')
        return f"Thermostat turned off"

    await therm.async_set_mode(mode)
    
    temp_celcius = int((temperature - 32) * (5/9))
    return f"Thermostat set to {temperature}°F/ {temp_celcius}°C in {mode} mode"

        