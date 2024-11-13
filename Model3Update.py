import os
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List
import open3d as o3d  
import numpy as np
import traci
import pickle
from PIL import Image
from rich import print

import dearpygui.dearpygui as dpg
import dearpygui_ext.themes as dpg_ext

from simModel.CarFactory import Vehicle, egoCar
from simModel.DataQueue import (
    CameraImages, ImageQueue, QAQueue, QuestionAndAnswer, RenderQueue,
)
from simModel.DBBridge import DBBridge
from simModel.MovingScene import MovingScene
from simModel.NetworkBuild import NetworkBuild
from utils.simBase import vehType
from utils.trajectory import Trajectory
import carla

class SettingErro(Exception):
    def __init__(self, errorInfo: str) -> None:
        super().__init__(self)
        self.errorInfo = errorInfo

    def __str__(self) -> str:
        return self.errorInfo

def resizeImage(img: np.ndarray, width: int, height: int) -> bytes:
    img = Image.fromarray(img)
    img_resized = img.resize((width, height))
    np_img_resized = np.array(img_resized)
    print(type(np_img_resized))
    return np_img_resized.tobytes()

class Model:
    def __init__(
        self, 
        egoID: str,
        netFile: str, rouFile: str, cfgFile: str,
        dataBase: str = None,
        SUMOGUI: bool = False, 
        CARLACosim: bool = True,
        carla_host: str = '127.0.0.1',
        carla_port: int = 2000,
        tls_manager: str = 'sumo'
    ) -> None:
        
        
        print('[green bold]Model initialized at {}.[/green bold]'.format(
            datetime.now().strftime('%H:%M:%S.%f')[:-3]))
        self.netFile = netFile
        self.rouFile = rouFile
        self.cfgFile = cfgFile
        self.SUMOGUI = SUMOGUI
        self.CARLACosim = CARLACosim
        self.carla_host = carla_host
        self.carla_port = carla_port
        self.tls_manager = tls_manager
        self.sim_mode: str = 'RealTime'
        self.timeStep = 0
        # tpStart marks whether the trajectory planning is started,
        # when the ego car appears in the network, tpStart turns into 1.
        self.tpStart = 0
        # tpEnd marks whether the trajectory planning is end,
        # when the ego car leaves the network, tpEnd turns into 1.
        self.tpEnd = 0

        self.ego = egoCar(egoID)

        if dataBase:
            self.dataBase = dataBase
        else:
            self.dataBase = datetime.strftime(
                datetime.now(), '%Y-%m-%d_%H-%M-%S') + '_egoTracking' + '.db'

        if os.path.exists(self.dataBase):
            os.remove(self.dataBase)
        self.dbBridge = DBBridge(self.dataBase)
        self.dbBridge.createTable()
        self.simDescriptionCommit()
        self.renderQueue = RenderQueue(5)
        self.imageQueue = ImageQueue(50)
        self.QAQ = QAQueue(5)

        self.nb = NetworkBuild(self.dataBase, netFile)
        self.nb.getData()
        self.nb.buildTopology()

        self.ms = MovingScene(self.nb, self.ego)

        self.allvTypes = None

        self.netBoundary = None
                
        #******************************************************************************************
    def set_weather(self,cloudiness=80.0, precipitation=70.0, 
                    precipitation_deposits=60.0, wind_intensity=30.0, 
                    sun_altitude_angle=45.0,
                    fog_density=10.0, fog_distance=10.0, wetness=80.0):  
        if self.carlaSync:
            weather = carla.WeatherParameters(
                cloudiness=cloudiness,
                precipitation=precipitation,
                precipitation_deposits=precipitation_deposits,
                wind_intensity=wind_intensity,
                sun_altitude_angle=sun_altitude_angle,
                fog_density=fog_density,
                fog_distance=fog_distance,
                wetness=wetness
               )
            #self.carlaSync.world.set_weather(weather)
            self.world.set_weather(weather)
        else:
            print("carlaSync is not initialized. Weather cannot be set.")
            
       #***********************************************************Added ******************************* 
        
    def getLidarData(self):
       
        return self.lidarData
    
    def lidar_callback(self, data):
        points = []
        object_ids = []
    
    # Process semantic LiDAR data
        for detection in data:
            point = [detection.point.x, detection.point.y, detection.point.z]
            points.append(point)
            object_ids.append(detection.object_tag)

    # Convert lists to numpy arrays for easier manipulation
        points = np.array(points)

    # Create an Open3D PointCloud
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(points)

    # Example: Downsample the point cloud
        downsampled_point_cloud = point_cloud.voxel_down_sample(voxel_size=0.1)

    # Example: Estimate normals
        downsampled_point_cloud.estimate_normals()

    # Extract bounding boxes for each cluster
        unique_labels = np.unique(object_ids)
        bounding_boxes = []
        for label in unique_labels:
            cluster_indices = np.where(object_ids == label)[0]
            cluster_points = points[cluster_indices]
            bbox = o3d.geometry.AxisAlignedBoundingBox.create_from_points(o3d.utility.Vector3dVector(cluster_points))
            bounding_boxes.append(bbox)

    # Extract some features
        num_points = len(points)
        distances = np.linalg.norm(points, axis=1)
        mean_distance = np.mean(distances)
        min_distance = np.min(distances)
        max_distance = np.max(distances)

    # Example: Check if there are any pedestrians in the vicinity
        labels = [self.get_label(tag) for tag in object_ids]
        pedestrians_in_vicinity = any(label == 'pedestrian' for label in labels)

    # Store the processed data
        processed_data = {
            'point_cloud': point_cloud,
            'bounding_boxes': bounding_boxes,
            'num_points': num_points,
            'mean_distance': mean_distance,
            'min_distance': min_distance,
            'max_distance': max_distance,
            'pedestrians_in_vicinity': pedestrians_in_vicinity
        }
        self.lidarData = processed_data

    def get_label(self, tag):
     label_map = {
         0: 'None',
         1: 'Building',
         2: 'Fence',
         3: 'Other',
         4: 'Pedestrian',
         5: 'Pole',
         6: 'RoadLine',
         7: 'Road',
         8: 'Sidewalk',
         9: 'Vegetation',
         10: 'Vehicles',
         11: 'Wall',
         12: 'TrafficSign',
         13: 'Sky',
         14: 'Ground',
         15: 'Bridge',
         16: 'RailTrack',
         17: 'GuardRail',
         18: 'TrafficLight',
         19: 'Static',
         20: 'Dynamic',
         21: 'Water',
         22: 'Terrain'
     }
     return label_map.get(tag, 'Unknown')
 
 
    def simDescriptionCommit(self):
        currTime = datetime.now()
        insertQuery = '''INSERT INTO simINFO VALUES (?, ?, ?);'''
        conn = sqlite3.connect(self.dataBase)
        cur = conn.cursor()
        cur.execute(
            insertQuery,
            (currTime, self.ego.id, '')
        )

        conn.commit()
        cur.close()
        conn.close()

    # DEFAULT_VEHTYPE
    def getAllvTypeID(self) -> list:
        allvTypesID = []
        if ',' in self.rouFile:
            vTypeFile = self.rouFile.split(',')[0]
            elementTree = ET.parse(vTypeFile)
            root = elementTree.getroot()
            for child in root:
                if child.tag == 'vType':
                    vtid = child.attrib['id']
                    allvTypesID.append(vtid)
        else:
            elementTree = ET.parse(self.rouFile)
            root = elementTree.getroot()
            for child in root:
                if child.tag == 'vType':
                    vtid = child.attrib['id']
                    allvTypesID.append(vtid)

        return allvTypesID

    def start(self):
        traci.start([
            'sumo-gui' if self.SUMOGUI else 'sumo',
            '-n', self.netFile,
            '-r', self.rouFile,
            '--step-length', '0.1',
            '--lateral-resolution', '10',
            '--start', '--quit-on-end',
            '-W'
        ])

        ((x1, y1), (x2, y2)) = traci.simulation.getNetBoundary()
        self.netBoundary = ((x1, y1), (x2, y2))
        netBoundaryStr = f"{x1},{y1} {x2},{y2}"
        conn = sqlite3.connect(self.dataBase)
        cur = conn.cursor()
        cur.execute(f"""UPDATE simINFO SET netBoundary = '{netBoundaryStr}';""")
        conn.commit()
        conn.close()

        allvTypeID = self.getAllvTypeID()
        allvTypes = {}
        if allvTypeID:
            for vtid in allvTypeID:
                vtins = vehType(vtid)
                vtins.maxAccel = traci.vehicletype.getAccel(vtid)
                vtins.maxDecel = traci.vehicletype.getDecel(vtid)
                vtins.maxSpeed = traci.vehicletype.getMaxSpeed(vtid)
                vtins.length = traci.vehicletype.getLength(vtid)
                vtins.width = traci.vehicletype.getWidth(vtid)
                vtins.vclass = traci.vehicletype.getVehicleClass(vtid)
                allvTypes[vtid] = vtins
        else:
            vtid = 'DEFAULT_VEHTYPE'
            vtins = vehType(vtid)
            vtins.maxAccel = traci.vehicletype.getAccel(vtid)
            vtins.maxDecel = traci.vehicletype.getDecel(vtid)
            vtins.maxSpeed = traci.vehicletype.getMaxSpeed(vtid)
            vtins.length = traci.vehicletype.getLength(vtid)
            vtins.width = traci.vehicletype.getWidth(vtid)
            vtins.vclass = traci.vehicletype.getVehicleClass(vtid)
            allvTypes[vtid] = vtins
            self.allvTypes = allvTypes
        self.allvTypes = allvTypes

        if self.CARLACosim:
            from sumo_integration.run_synchronization import getSynchronization
            self.carlaSync = getSynchronization(
                sumo_cfg_file=self.cfgFile,
                carla_host=self.carla_host,
                carla_port=self.carla_port,
                ego_id=self.ego.id,
                step_length=0.1,
                tls_manager=self.tls_manager,
                sync_vehicle_color=True,
                sync_vehicle_lights=True
            )
            #****************************************** Added ****************************************
            self.world = self.carlaSync.carla.world
            
            self.blueprint_library = self.world.get_blueprint_library()
            
            
            lidar_bp = self.blueprint_library.find('sensor.lidar.ray_cast_semantic')
            lidar_bp.set_attribute('range', '100.0')
            lidar_bp.set_attribute('rotation_frequency', '10')
            lidar_bp.set_attribute('channels', '32')
            lidar_bp.set_attribute('points_per_second', '56000')
            
            lidar_transform = carla.Transform(carla.Location(x=0, y=0, z=2.5))  # Adjust the location as necessary
            self.lidar_sensor = self.world.spawn_actor(lidar_bp, lidar_transform)
            self.lidar_sensor.listen(lambda data: self.lidar_callback(data))
            self.lidarData = None
           #****************************************** Added *****************************************
            #self.set_weather(cloudiness=70.0, precipitation=0.0, precipitation_deposits=0.0, wind_intensity=5.0, sun_altitude_angle=30.0, fog_density=90.0, fog_distance=1.0, wetness=30.0)  # <-- Added line by sonda******************************
            self.set_weather(cloudiness=00.0, precipitation=00.0, precipitation_deposits=00.0, wind_intensity=10.0, sun_altitude_angle=65.0, fog_density=00.0, fog_distance=.30, wetness=00.0)  # <-- Added line by sonda***********Snow*************
            
            #****************************************** Added *****************************************
        else:
            return

    def commitFrameInfo(self, vid: str, vtag: str, veh: Vehicle):
        self.dbBridge.putData(
            'frameINFO',
            (
                self.timeStep, vid, vtag, veh.x, veh.y, veh.yaw, veh.speed,
                veh.accel, veh.laneID, veh.lanePos, veh.routeIdxQ[-1]
            )
        )


    def commitVehicleInfo(self, vid: str, vtins: vehType, routes: str):
        self.dbBridge.putData(
            'vehicleINFO', 
            (
                vid, vtins.length, vtins.width, vtins.maxAccel,
                vtins.maxDecel, vtins.maxSpeed, vtins.id, routes
            )
        )

    def putVehicleINFO(self):
        self.commitFrameInfo(self.ego.id, 'ego', self.ego)
        if self.ms.vehINAoI:
            for v1 in self.ms.vehINAoI.values():
                self.commitFrameInfo(v1.id, 'AoI', v1)
        if self.ms.outOfAoI:
            for v2 in self.ms.outOfAoI.values():
                try:
                    self.commitFrameInfo(v2.id, 'outOfAoI', v2)
                except TypeError:
                    return

    def getvTypeIns(self, vtid: str) -> vehType:
        return self.allvTypes[vtid]

    def getVehInfo(self, veh: Vehicle):
        vid = veh.id
        if veh.vTypeID:
            max_decel = veh.maxDecel
        else:
            vtypeid: str = traci.vehicle.getTypeID(vid)
            if '@' in vtypeid:
                vtypeid = vtypeid.split('@')[0]
            vtins = self.getvTypeIns(vtypeid)
            veh.maxAccel = vtins.maxAccel
            veh.maxDecel = vtins.maxDecel
            veh.length = vtins.length
            veh.width = vtins.width
            veh.maxSpeed = vtins.maxSpeed
            # veh.targetCruiseSpeed = random.random()
            veh.vTypeID = vtypeid
            veh.routes = traci.vehicle.getRoute(vid)
            veh.LLRSet, veh.LLRDict, veh.LCRDict = veh.getLaneLevelRoute(
                self.nb)

            routes = ' '.join(veh.routes)
            self.commitVehicleInfo(vid, vtins, routes)
            max_decel = veh.maxDecel
        veh.yawAppend(traci.vehicle.getAngle(vid))
        x, y = traci.vehicle.getPosition(vid)
        veh.xAppend(x)
        veh.yAppend(y)
        veh.speedQ.append(traci.vehicle.getSpeed(vid))
        if max_decel == traci.vehicle.getDecel(vid):
            accel = traci.vehicle.getAccel(vid)
        else:
            accel = -traci.vehicle.getDecel(vid)
        veh.accelQ.append(accel)
        laneID = traci.vehicle.getLaneID(vid)
        veh.routeIdxAppend(laneID)
        veh.laneAppend(self.nb)

    def vehMoveStep(self, veh: Vehicle):
        # control vehicles after update its data
        # control happens next timestep
        if veh.plannedTrajectory and veh.plannedTrajectory.xQueue:
            centerx, centery, yaw, speed, accel = veh.plannedTrajectory.pop_last_state(
            )
            try:
                veh.controlSelf(centerx, centery, yaw, speed, accel)
            except:
                return
        else:
            veh.exitControlMode()

    def updateVeh(self):
        self.vehMoveStep(self.ego)
        if self.ms.currVehicles:
            for v in self.ms.currVehicles.values():
                self.vehMoveStep(v)

    def setTrajectories(self, trajectories: Dict[str, Trajectory]):
        for k, v in trajectories.items():
            if k == self.ego.id:
                self.ego.plannedTrajectory = v
            else:
                veh = self.ms.currVehicles[k]
                veh.plannedTrajectory = v

    def getSce(self):
        if self.ego.id in traci.vehicle.getIDList():
            self.tpStart = 1
            self.ms.updateScene(self.dbBridge, self.timeStep)
            self.ms.updateSurroudVeh()

            self.getVehInfo(self.ego)
            if self.ms.currVehicles:
                for v in self.ms.currVehicles.values():
                    self.getVehInfo(v)

            self.putVehicleINFO()
        else:
            if self.tpStart:
                print('[cyan]The ego car has reached the destination.[/cyan]')
                self.tpEnd = 1

        if self.tpStart:
            if self.ego.arriveDestination(self.nb):
                self.tpEnd = 1
                print('[cyan]The ego car has reached the destination.[/cyan]')

    def putRenderData(self):
        if self.tpStart:
            roadgraphRenderData, VRDDict = self.ms.exportRenderData()
            self.renderQueue.put((roadgraphRenderData, VRDDict))

    def exportSce(self):
        if self.tpStart:
            return self.ms.exportScene()
        else:
            return None, None
        
    def putCARLAImage(self):
        if self.CARLACosim:
            carla_ego = self.carlaSync.getEgo()
            if carla_ego:
                self.carlaSync.moveSpectator(carla_ego)
                self.carlaSync.setCameras(carla_ego)
                ci = self.carlaSync.getCameraImages()
                if ci:
                    ci.resizeImage(450, 315)
                    self.imageQueue.put(ci)
                    self.dbBridge.putData(
                        'imageINFO',
                        (
                            self.timeStep, 
                            sqlite3.Binary(pickle.dumps(ci.CAM_FRONT)),
                            sqlite3.Binary(pickle.dumps(ci.CAM_FRONT_RIGHT)),
                            sqlite3.Binary(pickle.dumps(ci.CAM_FRONT_LEFT)),
                            sqlite3.Binary(pickle.dumps(ci.CAM_BACK_LEFT)),
                            sqlite3.Binary(pickle.dumps(ci.CAM_BACK)),
                            sqlite3.Binary(pickle.dumps(ci.CAM_BACK_RIGHT))
                        )
                    )
        else:
            return
        
    def getCARLAImage(
            self, start_frame: int, steps: int=1
        ) -> List[CameraImages]:
        return self.imageQueue.get(start_frame, steps)
        
    def putQA(self, QA: QuestionAndAnswer):
        self.QAQ.put(QA)
        self.dbBridge.putData(
            'QAINFO',
            (
                self.timeStep, QA.description, QA.navigation,
                QA.actions, QA.few_shots, QA.response,
                QA.prompt_tokens, QA.completion_tokens, QA.total_tokens, QA.total_time,  QA.choose_action
            )
        )

    def moveStep(self):
        traci.simulationStep()
        if self.CARLACosim:
            self.carlaSync.tick()
        self.timeStep += 1
        if self.ego.id in traci.vehicle.getIDList():
            self.getSce()
            self.putRenderData()
            self.putCARLAImage()
            if not self.tpStart:
                self.tpStart = 1
            
    def destroy(self):
        traci.close()
        self.dbBridge.close()
        if self.CARLACosim:
            self.carlaSync.close()
