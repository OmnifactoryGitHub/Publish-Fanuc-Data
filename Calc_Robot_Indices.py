import numpy as np

Energy_Cost_Per_kWh = 21.65 #pence per kWh - unit rate

def compute_energy_cost(current_fields, previous_cost, dt):
    power = current_fields['power']
    energy = power/1e3 * dt/36000
    cost = energy * Energy_Cost_Per_kWh/100 # In pounds
    return {
        "cost": cost,
        "energy": energy, # kWh
        "cummulative_cost": previous_cost + cost
    }

def compute_velocity(previous_fields, current_fields, dt):
    return {
        "vx": (current_fields['X']-previous_fields['X']) / dt,
        "vy": (current_fields['Y']-previous_fields['Y']) / dt,
        "vz": (current_fields['Z']-previous_fields['Z']) / dt,
        'vw': (current_fields['W']-previous_fields['W']) / dt,
        'vp': (current_fields['P']-previous_fields['P']) / dt,
        'vr': (current_fields['R']-previous_fields['R']) / dt,
    }


def compute_acceleration(previous_velocity, current_velocity, dt):
    if previous_velocity is None:
        return {
            "ax": None,
            "ay": None,
            "az": None,
            'aw': None,
            'ap': None,
            'ar': None,
        }
    else:
        return {
            "ax": (current_velocity['vx']-previous_velocity['vx'])/dt,
            "ay": (current_velocity['vy']-previous_velocity['vy'])/dt,
            "az": (current_velocity['vz']-previous_velocity['vz'])/dt,
            'aw': (current_velocity['vw']-previous_velocity['vw']) / dt,
            'ap': (current_velocity['vp']-previous_velocity['vp']) / dt,
            'ar': (current_velocity['vr']-previous_velocity['vr']) / dt,
        }