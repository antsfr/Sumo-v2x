import traci

from sumoRetriever import manage_NMEA


def make_step(config, sock, results):
    traci.simulationStep()
    manage_NMEA(config, sock, results)


def longitudinal_collision(config, sock, results):
    make_step(config, sock, results)
    traci.vehicle.setSpeed("veh0", 8)
    traci.vehicle.changeLane("veh1", 1, 10)
    for _ in range(5):
        make_step(config, sock, results)
    traci.vehicle.changeLane("veh1", 0,  30)
    traci.vehicle.setSpeed("veh0", 8)


def longitudinal_collision_N(config, sock, results):
    make_step(config, sock, results)
    traci.vehicle.setSpeed("veh1", 40)
    traci.vehicle.setSpeedMode("veh0", 32)
    traci.vehicle.setSpeedMode("veh1", 32)


def intersection_collision(config, sock, results):
    make_step(config, sock, results)


def intersection_collision_N(config, sock, results):
    for step in range(30):
        make_step(config, sock, results)
    traci.simulationStep()
    manage_NMEA(config, sock, results)
    traci.vehicle.changeLane("veh1", 0, 5)
    traci.vehicle.setDecel("veh1", 0)


def signal_violation(config, sock, results):
    make_step(config, sock, results)


def signal_violation_N(config, sock, results):
    make_step(config, sock, results)