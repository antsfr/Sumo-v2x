import os, sys
from datetime import datetime
import socket
from time import sleep
import pynmea2
import traci
import traci.constants as tc
import yaml
from sumolib import checkBinary
import scenarios


def convert_coordinates(latitude, longitude):
    latitude, longitude = abs(latitude), abs(longitude)
    lat_degrees = str(int(latitude))
    long_degrees = (str(int(longitude)))
    if len(long_degrees) == 1:
        long_degrees = '00' + long_degrees
    if len(lat_degrees) == 1:
        lat_degrees = '0' + lat_degrees
    elif len(long_degrees) == 2:
        long_degrees = '0' + long_degrees
    lat_minutes = str((latitude - int(latitude)) * 60)
    long_minutes = str((longitude - int(longitude)) * 60)
    if float(lat_minutes) - 10 < 0:
        if float(lat_minutes) == 0:
            lat_minutes = '00.00'
        else:
            lat_minutes = '0' + lat_minutes
    if float(long_minutes) - 10 < 0:
        if float(long_minutes) == 0:
            long_minutes = '00.00'
        else:
            long_minutes = '0' + long_minutes
    latitude = lat_degrees + lat_minutes[:7]
    longitude = long_degrees + long_minutes[:7]
    return latitude, longitude


def traci_init(config):
    if (config['GUI']):
        sumo = "sumo-gui"
    else:
        sumo = "sumo"
    traci.start([sumo, "-c", "scenarios/" + config['scenario'] + "/" + config['filename'] + ".sumocfg"])
    for i in range(len(config['vehID'])):
        traci.vehicle.subscribe(config['vehID'][i], (tc.VAR_ROAD_ID, tc.VAR_SPEED_WITHOUT_TRACI, tc.VAR_POSITION))
        traci.trafficlight.subscribe(config['tlID'][i], (tc.TL_CURRENT_PHASE, tc.TL_PHASE_DURATION))


def traci_terminate():
    traci.close()


def create_connection(i):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = (config["hostname"][i], config["port"][i])
    return sock, address


def generate_NMEA(i, config, results):
    x, y = traci.vehicle.getPosition(config['vehID'][i])
    longitude_for_convert, latitude_for_convert = traci.simulation.convertGeo(x, y)
    if abs(longitude_for_convert) > 180 or abs(latitude_for_convert) > 90:
        print("VEHICLE NOT FOUND")
        print("VEHICLE NOT FOUND", file=results)
        return ""
    latitude, longitude = convert_coordinates(latitude_for_convert, longitude_for_convert)
    clock = datetime.now().utcnow()
    lat_part = 'N' if latitude_for_convert >= 0 else 'S'
    long_part = 'E' if longitude_for_convert >= 0 else 'W'
    velocity = traci.vehicle.getSpeed(config['vehID'][i])
    result_azimuth = traci.vehicle.getAngle(config['vehID'][i])
    msg = str(pynmea2.RMC('GP', 'RMC', (clock.strftime('%H%M%S.%f')[:-4], 'A', latitude, lat_part, longitude,
                                        long_part, '%02d.1' % (velocity * 1.94384), '%03d.1' % result_azimuth,
                                        clock.strftime('%d%m%y'), '011.3,E')))
    # yield msg
    print(msg, file=results)
    print(msg)

    if config['TLRetrieval']:
        # print(traci.trafficlight.getPhase(config['tlID'][i]))
        # print(traci.trafficlight.getRedYellowGreenState(config['tlID'][i]))
        print(traci.trafficlight.getCompleteRedYellowGreenDefinition(config['tlID'][i]))
        pass
    signals = "{0:b}".format(traci.vehicle.getSignals(config['vehID'][i]))
    print(signals.zfill(13))

    return msg


def send_NMEA(config, sock, address, msg):
    sock.sendto(bytes(msg, 'utf-8'), address)
    sleep(config["NMEAFreq"])


def manage_NMEA(config, sock, results):
    for i in range(len(config['vehID'])):
        print("vehID:", i)
        msg = generate_NMEA(i, config, results)
        send_NMEA(config, sock, (config["hostname"][i], config["port"][i]), msg)


if __name__ == "__main__":
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    results = open("results.txt", "w")
    os.environ["SUMO_HOME"] = config['sumoPath']
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")
    sumoBinary = checkBinary('sumo-gui')
    sumoCmd = [sumoBinary + " -c" + " resources/" + config['filename'] + ".sumocfg"]

    traci_init(config)
    sock = None
    address = ("", 0)
    sock, address = create_connection(0)
    msg = ""
    for step in range(config['steps']):
        getattr(scenarios, config["scenario"])(config, sock, results)
        # print("step:", step)
        #print("step:", step, ",vehID:", i, file=results)
        # manage_NMEA(config, sock)
    sock.close()
    results.close()
    traci_terminate()
