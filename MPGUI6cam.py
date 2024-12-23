# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 18:01:21 2024

@author: Fourati
"""

import os
from math import cos, pi, sin
from multiprocessing import Process
from typing import Dict, List, Tuple

import dearpygui.dearpygui as dpg
import dearpygui_ext.themes as dpg_ext
import numpy as np
from matplotlib import pyplot as plt
from rich import print

from simModel.DataQueue import (
    ERD, JLRD, LRD, RGRD, VRD, CameraImages, QuestionAndAnswer,
)
from simModel.Model3 import Model
from utils.simBase import CoordTF



class SequenceError(Exception):
    def __init__(self, errorInfo: str) -> None:
        super().__init__(self)
        self.errorInfo = errorInfo

    def __str__(self) -> str:
        return self.errorInfo
    

def generateDefaultImage(
    width, height, bgcolor='white', 
    text='No Signal', fontcolor='black'
) -> List:
    # 创建一个新的图像
    fig, ax = plt.subplots(figsize=(width/80, height/80), dpi=80)
    
    # 设置背景颜色
    fig.patch.set_facecolor(bgcolor)
    
    # 移除坐标轴
    ax.axis('off')
    
    # 在图像中心添加文本
    ax.text(0.5, 0.5, text, fontsize=30, ha='center', va='center', color=fontcolor)
    
    # 将图像转换为 NumPy 数组
    fig.canvas.draw()
    np_img = np.array(fig.canvas.renderer.buffer_rgba())
    
    # 关闭图像，释放资源
    plt.close(fig)
    
    # 归一化并展平图像
    np_img = np_img / 255
    return np_img.flatten().tolist()

class GUI(Process):
    def __init__(
        self, model: Model,
    ) -> None:
        super().__init__()
        self.renderQueue = model.renderQueue
        self.imageQueue = model.imageQueue
        self.QAQ = model.QAQ
        if model.netBoundary:
            self.netBoundary = model.netBoundary
        else:
            raise SequenceError(
                'Class `GUI` must be initialized after `model.start()`.'
            )

        self.zoom_speed: float = 1.0
        self.is_dragging: bool = False
        self.old_offset = (0, 0)
 
    def setup(self):
        dpg.create_context()
        dpg.create_viewport(
            title="TrafficSimulator",
            width=1910, height=1230)   # ***************for the scenario of four cameras
           # width=1800, height=1230)  # ***************for the scenario of three cameras
        dpg.setup_dearpygui()

    def setup_themes(self):
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding, 3,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameBorderSize, 0.5,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_WindowBorderSize, 0,
                    category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvNodeCol_NodeBackground, (255, 255, 255)
                )

        dpg.bind_theme(global_theme)

    def create_windows(self):
        with dpg.font_registry():
            font_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), ".", "fonts", "Meslo.ttf"
            )
            default_font = dpg.add_font(font_path, 18)
            self.font2 = dpg.add_font(font_path, 20)

        dpg.bind_font(default_font)

        # Camera Window
        image_width = 450  # ***************Modified for the scenario of four cameras
        # image_width = 560  # ***************Modified  for the scenario of three cameras
        image_height = 315
        ## CAM_FRONT_LEFT
        self.CAM_FRONT_LEFT_TR = dpg.add_texture_registry(show=False)
        dpg.add_dynamic_texture(
            width=image_width, height=image_height, 
            default_value=generateDefaultImage(image_width, image_height),
            tag='CAM_FRONT_LEFT_TT', parent=self.CAM_FRONT_LEFT_TR
        )
        with dpg.window(tag='CAM_FRONT_LEFT_WINDOW', label='CAM_FRONT_LEFT'):
            dpg.add_image('CAM_FRONT_LEFT_TT')

        ## CAM_FRONT
        self.CAM_FRONT_TR = dpg.add_texture_registry(show=False)
        dpg.add_dynamic_texture(
            width=image_width, height=image_height, 
            default_value=generateDefaultImage(image_width, image_height),
            tag='CAM_FRONT_TT', parent=self.CAM_FRONT_TR
        )
        with dpg.window(tag='CAM_FRONT_WINDOW', label='CAM_FRONT'):
            dpg.add_image('CAM_FRONT_TT')

        ## CAM_FRONT_RIGHT
        self.CAM_FRONT_RIGHT_TR = dpg.add_texture_registry(show=False)
        dpg.add_dynamic_texture(
            width=image_width, height=image_height,
            default_value=generateDefaultImage(image_width, image_height),
            tag='CAM_FRONT_RIGHT_TT', parent=self.CAM_FRONT_RIGHT_TR
        )
        with dpg.window(tag='CAM_FRONT_RIGHT_WINDOW', label='CAM_FRONT_RIGHT'):
            dpg.add_image('CAM_FRONT_RIGHT_TT')
#*******************************ADDED for the scenario of six cameras******************************
        ## CAM_BACK_LEFT
        self.CAM_BACK_LEFT_TR = dpg.add_texture_registry(show=False)
        dpg.add_dynamic_texture(
            width=image_width, height=image_height, 
            default_value=generateDefaultImage(image_width, image_height),
            tag='CAM_BACK_LEFT_TT', parent=self.CAM_BACK_LEFT_TR
        )
        with dpg.window(tag='CAM_BACK_LEFT_WINDOW', label='CAM_BACK_LEFT'):
            dpg.add_image('CAM_BACK_LEFT_TT') 

    
     ## CAM_BACK
        self.CAM_BACK_TR = dpg.add_texture_registry(show=False)
        dpg.add_dynamic_texture(
             width=image_width, height=image_height, 
             default_value=generateDefaultImage(image_width, image_height),
             tag='CAM_BACK_TT', parent=self.CAM_BACK_TR
        )
        with dpg.window(tag='CAM_BACK_WINDOW', label='CAM_BACK'):
             dpg.add_image('CAM_BACK_TT')
            
                           
         ## CAM_BACK_RIGHT
        self.CAM_BACK_RIGHT_TR = dpg.add_texture_registry(show=False)
        dpg.add_dynamic_texture(
             width=image_width, height=image_height,
             default_value=generateDefaultImage(image_width, image_height),
             tag='CAM_BACK_RIGHT_TT', parent=self.CAM_BACK_RIGHT_TR
         )
        with dpg.window(tag='CAM_BACK_RIGHT_WINDOW', label='CAM_BACK_RIGHT'):
             dpg.add_image('CAM_BACK_RIGHT_TT')
#***************************************************************************************************
        
        # Prompts windows
        dpg.add_window(tag="PromptsWindow", label='Prompts')
        
        light_theme = dpg_ext.create_theme_imgui_light()
        dpg.bind_theme(light_theme)
        
        # BEV Window
        dpg.add_window(tag="BEVWindow", label="BEV View")
        dpg.add_draw_node(tag="CanvasBG", parent="BEVWindow")
        dpg.add_draw_node(tag="Canvas", parent="BEVWindow")
        
        # Response Window
        dpg.add_window(tag="ResponseWindow", label='Reasoning and decision')

    def create_handlers(self):
        with dpg.handler_registry():
            dpg.add_mouse_down_handler(callback=self.mouse_down)
            dpg.add_mouse_drag_handler(callback=self.mouse_drag)
            dpg.add_mouse_release_handler(callback=self.mouse_release)
            dpg.add_mouse_wheel_handler(callback=self.mouse_wheel)
#********************************************************************Modified  for four cameras : Resize_Window *********************************************
    def resize_windows(self):
        dpg.set_item_width("CAM_FRONT_LEFT_WINDOW", 460)  # ***************Modified for the scenario of four cameras 460 instead of 560
        dpg.set_item_height("CAM_FRONT_LEFT_WINDOW", 360)
        dpg.set_item_pos("CAM_FRONT_LEFT_WINDOW", (10, 10))

        dpg.set_item_width('CAM_FRONT_WINDOW', 460)    # ***************Modified  for the scenario of four cameras 460 instead of 560
        dpg.set_item_height('CAM_FRONT_WINDOW', 360)
        dpg.set_item_pos('CAM_FRONT_WINDOW', (10, 370)) # ***************Modified for the scenario of four cameras 480 instead of 600

        dpg.set_item_width('CAM_FRONT_RIGHT_WINDOW', 460)  # ***************Modified for the scenario of four cameras 460 instead of 560
        dpg.set_item_height('CAM_FRONT_RIGHT_WINDOW', 360)
        dpg.set_item_pos('CAM_FRONT_RIGHT_WINDOW', (10, 730))   # ***************Modified for the scenario of four cameras 950 instead of 1190
       #*******************Added  for the six  camera scenario************************************ 
        dpg.set_item_width('CAM_BACK_LEFT_WINDOW', 460)   
        dpg.set_item_height('CAM_BACK_LEFT_WINDOW', 360)
        dpg.set_item_pos('CAM_BACK_LEFT_WINDOW', (480, 10))  
        
     
        dpg.set_item_width('CAM_BACK_WINDOW', 460)   
        dpg.set_item_height('CAM_BACK_WINDOW', 360)
        dpg.set_item_pos('CAM_BACK_WINDOW', (480, 370)) 
        
        
        dpg.set_item_width('CAM_BACK_RIGHT_WINDOW', 460)   
        dpg.set_item_height('CAM_BACK_RIGHT_WINDOW', 360)
        dpg.set_item_pos('CAM_BACK_RIGHT_WINDOW', (480, 730))  
        #*************************************************************************
        
        dpg.set_item_width('PromptsWindow', 440)
        dpg.set_item_height('PromptsWindow', 540)
        dpg.set_item_pos('PromptsWindow', (1480, 10))

        dpg.set_item_width('BEVWindow', 540)
        dpg.set_item_height('BEVWindow', 540)
        dpg.set_item_pos('BEVWindow', (940, 10))

        dpg.set_item_width('ResponseWindow', 980)
        dpg.set_item_height('ResponseWindow', 540)
        dpg.set_item_pos('ResponseWindow', (940, 560))
#*************************************************************Resize Window for 3 cameras **************************************************
   # def resize_windows(self):
     #    dpg.set_item_width("CAM_FRONT_LEFT_WINDOW", 580)
     #    dpg.set_item_height("CAM_FRONT_LEFT_WINDOW", 360)
      #   dpg.set_item_pos("CAM_FRONT_LEFT_WINDOW", (10, 10))

      #   dpg.set_item_width('CAM_FRONT_WINDOW', 580)
      #   dpg.set_item_height('CAM_FRONT_WINDOW', 360)
      #   dpg.set_item_pos('CAM_FRONT_WINDOW', (600, 10))

      #   dpg.set_item_width('CAM_FRONT_RIGHT_WINDOW', 580)
      #   dpg.set_item_height('CAM_FRONT_RIGHT_WINDOW', 360)
      #   dpg.set_item_pos('CAM_FRONT_RIGHT_WINDOW', (1190, 10))

      #   dpg.set_item_width('PromptsWindow', 470)
      #   dpg.set_item_height('PromptsWindow', 800)
     #    dpg.set_item_pos('PromptsWindow', (10, 380))

     #    dpg.set_item_width('BEVWindow', 800)
     #    dpg.set_item_height('BEVWindow', 800)
     #    dpg.set_item_pos('BEVWindow', (490, 380))

     #    dpg.set_item_width('ResponseWindow', 470)
     #    dpg.set_item_height('ResponseWindow', 800)
      #   dpg.set_item_pos('ResponseWindow', (1300, 380))
#****************************************************************************************************************************************


    def drawMainWindowWhiteBG(self):
        pmin, pmax =  self.netBoundary
        centerx = (pmin[0] + pmax[0]) / 2
        centery = (pmin[1] + pmax[1]) / 2
        dpg.draw_rectangle(
            self.ctf.dpgCoord(pmin[0], pmin[1], centerx, centery),
            self.ctf.dpgCoord(pmax[0], pmax[1], centerx, centery),
            thickness=0,
            fill=(255, 255, 255),
            parent="CanvasBG"
        )

    def mouse_down(self):
        if not self.is_dragging:
            if dpg.is_item_hovered("BEVWindow"):
                self.is_dragging = True
                self.old_offset = self.ctf.offset

    def mouse_drag(self, sender, app_data):
        if self.is_dragging:
            self.ctf.offset = (
                self.old_offset[0] + app_data[1]/self.ctf.zoomScale,
                self.old_offset[1] + app_data[2]/self.ctf.zoomScale
            )

    def mouse_release(self):
        self.is_dragging = False

    def mouse_wheel(self, sender, app_data):
        if dpg.is_item_hovered("BEVWindow"):
            self.zoom_speed = 1 + 0.01*app_data

    def update_inertial_zoom(self, clip=0.005):
        if self.zoom_speed != 1:
            self.ctf.dpgDrawSize *= self.zoom_speed
            self.zoom_speed = 1+(self.zoom_speed - 1) / 1.05
        if abs(self.zoom_speed - 1) < clip:
            self.zoom_speed = 1

    def plotVehicle(self, node, ex: float, ey: float, vtag: str, vrd: VRD):
        rotateMat = np.array(
            [
                [cos(vrd.yaw), -sin(vrd.yaw)],
                [sin(vrd.yaw), cos(vrd.yaw)]
            ]
        )
        vertexes = [
            np.array([[vrd.length/2], [vrd.width/2]]),
            np.array([[vrd.length/2], [-vrd.width/2]]),
            np.array([[-vrd.length/2], [-vrd.width/2]]),
            np.array([[-vrd.length/2], [vrd.width/2]])
        ]
        rotVertexes = [np.dot(rotateMat, vex) for vex in vertexes]
        relativeVex = [
            [vrd.x+rv[0]-ex, vrd.y+rv[1]-ey] for rv in rotVertexes
        ]
        drawVex = [
            [
                self.ctf.zoomScale*(self.ctf.drawCenter+rev[0]+self.ctf.offset[0]),
                self.ctf.zoomScale*(self.ctf.drawCenter-rev[1]+self.ctf.offset[1])
            ] for rev in relativeVex
        ]
        if vtag == 'ego':
            vcolor = (211, 84, 0)
        elif vtag == 'AoI':
            vcolor = (41, 128, 185)
        else:
            vcolor = (99, 110, 114)

        dpg.draw_polygon(drawVex, color=vcolor, fill=vcolor, parent=node)
        dpg.draw_text(
            self.ctf.dpgCoord(vrd.x, vrd.y, ex, ey),
            vrd.id,
            color=(0, 0, 0),
            size=20,
            parent=node
        )

    def plotdeArea(self, node, egoVRD: VRD, ex: float, ey: float):
        cx, cy = self.ctf.dpgCoord(egoVRD.x, egoVRD.y, ex, ey)
        try:
            dpg.draw_circle(
                (cx, cy),
                self.ctf.zoomScale * egoVRD.deArea,
                thickness=2,
                fill=(243, 156, 18),
                parent=node
            )
        except Exception as e:
            raise e

    def plotTrajectory(self, node, ex: float, ey: float, vrd: VRD):
        tps = [
            self.ctf.dpgCoord(
                vrd.trajectoryXQ[i],
                vrd.trajectoryYQ[i],
                ex, ey
            ) for i in range(len(vrd.trajectoryXQ))
        ]
        dpg.draw_polyline(
            tps, color=(205, 132, 241),
            parent=node, thickness=2
        )

    def drawVehicles(
        self, node, VRDDict:Dict[str, List[VRD]], ex: float, ey: float
    ):
        egoVRD = VRDDict['egoCar'][0]
        self.plotVehicle(node, ex, ey, 'ego', egoVRD)
        # self.plotdeArea(node, egoVRD, ex, ey)
        if egoVRD.trajectoryXQ:
            self.plotTrajectory(node, ex, ey, egoVRD)
        for avrd in VRDDict['carInAoI']:
            self.plotVehicle(node, ex, ey, 'AoI', avrd)
            if avrd.trajectoryXQ:
                self.plotTrajectory(node, ex, ey, avrd)
        for svrd in VRDDict['outOfAoI']:
            self.plotVehicle(node, ex, ey, 'other', svrd)
    
    def get_line_tf(self, line: List[float], ex, ey) -> List[float]:
        return [
            self.ctf.dpgCoord(wp[0], wp[1], ex, ey) for wp in line
        ]
    
    def drawLane(self, node, lrd: LRD, ex, ey, flag: int):
        if flag & 0b10:
            return
        else:
            left_bound_tf = self.get_line_tf(lrd.left_bound, ex, ey)
            dpg.draw_polyline(
                left_bound_tf, color=(0, 0, 0, 100), 
                thickness=2, parent=node
            )

    def drawEdge(self, node, erd: ERD, rgrd: RGRD, ex, ey):
        for lane_index in range(erd.num_lanes):
            lane_id = erd.id + '_' + str(lane_index)
            lrd = rgrd.get_lane_by_id(lane_id)
            flag = 0b00
            if  lane_index == 0:
                flag += 1
                right_bound_tf = self.get_line_tf(lrd.right_bound, ex, ey)
            if lane_index == erd.num_lanes - 1:
                flag += 2
                left_bound_tf = self.get_line_tf(lrd.left_bound, ex, ey)
            self.drawLane(node, lrd, ex, ey, flag)

        left_bound_tf.reverse()
        right_bound_tf.extend(left_bound_tf)
        right_bound_tf.append(right_bound_tf[0])
        dpg.draw_polygon(
            right_bound_tf, color=(0, 0, 0),
            thickness=2, fill=(0, 0, 0, 30), parent=node
        )

    def drawJunctionLane(self, node, jlrd: JLRD, ex, ey):
        if jlrd.center_line:
            center_line_tf = self.get_line_tf(jlrd.center_line, ex, ey)
            if jlrd.currTlState:
                if jlrd.currTlState == 'r':
                    # jlColor = (232, 65, 24)
                    jlColor = (255, 107, 129, 100)
                elif jlrd.currTlState == 'y':
                    jlColor = (251, 197, 49, 100)
                elif jlrd.currTlState == 'g' or jlrd.currTlState == 'G':
                    jlColor = (39, 174, 96, 50)
            else:
                jlColor = (0, 0, 0, 30)
            dpg.draw_polyline(
                center_line_tf, color=jlColor,
                thickness=17,  parent=node
            )
        
    def drawRoadgraph(self, node, rgrd: RGRD, ex, ey):
        for erd in rgrd.edges.values():
            self.drawEdge(node, erd, rgrd, ex, ey)

        for jlrd in rgrd.junction_lanes.values():
            self.drawJunctionLane(node, jlrd, ex, ey)

    def showImage(self, cameraImages: CameraImages):
        front_left_image = cameraImages.CAM_FRONT_LEFT / 255
        dpg.set_value(
            'CAM_FRONT_LEFT_TT', front_left_image.flatten().tolist()
        )
        front_image = cameraImages.CAM_FRONT / 255
        dpg.set_value(
            'CAM_FRONT_TT', front_image.flatten().tolist()
        )
        front_right_image = cameraImages.CAM_FRONT_RIGHT / 255
        dpg.set_value(
            'CAM_FRONT_RIGHT_TT', front_right_image.flatten().tolist()
        )
       #********************************* Added for six cameras scenarios****************************************
        back_left_image = cameraImages.CAM_BACK_LEFT / 255
        dpg.set_value(
            'CAM_BACK_LEFT_TT', back_left_image.flatten().tolist()
        )
        back_image = cameraImages.CAM_BACK / 255
        dpg.set_value(
            'CAM_BACK_TT', back_image.flatten().tolist()
        )
        back_right_image = cameraImages.CAM_BACK_RIGHT / 255
        dpg.set_value(
            'CAM_BACK_RIGHT_TT', back_right_image.flatten().tolist()
        )
       
                #******************************************************************************
    def showPrompts(self, prompts: str):
        dpg.delete_item('descriptionTitle')
        dpg.delete_item('navigationTitle')
        dpg.delete_item('actionsTitle')
        dpg.delete_item('description')
        dpg.delete_item('navigation')
        dpg.delete_item('actions')
        a1 = dpg.add_text("## Description:\n", parent='PromptsWindow',
            tag='descriptionTitle', wrap=455, color=(0, 0, 255, 255))

        dpg.add_text(
            prompts["description"].replace("### ", "\n").strip("\n"), parent='PromptsWindow',
            tag='description', wrap=455)
        
        a2 = dpg.add_text("## Navigation:\n", parent='PromptsWindow',
            tag='navigationTitle', wrap=455, color=(0, 0, 255, 255))
        dpg.add_text(
            prompts["navigation"], parent='PromptsWindow',
            tag='navigation', wrap=455)
        
        a3 = dpg.add_text("## Actions:\n", parent='PromptsWindow',
            tag='actionsTitle', wrap=455, color=(0, 0, 255, 255))
        dpg.add_text(
            prompts["actions"], parent='PromptsWindow',
            tag='actions', wrap=455)
        
        dpg.bind_item_font(a1, self.font2)
        dpg.bind_item_font(a2, self.font2)
        dpg.bind_item_font(a3, self.font2)
    
    def showResponse(self, response: str):
        dpg.delete_item('response')
        dpg.delete_item('result')
        dpg.add_text(
            response.replace(response.strip("\n").split("\n")[-1], ""), parent='ResponseWindow', 
            tag='response', wrap=860, show = True,    #*****◘******************************************************Modified y Sonda ******************
            )
        result = dpg.add_text(
            response.strip("\n").split("\n")[-1], parent='ResponseWindow', 
            tag='result', wrap=880, show = True, color=(255, 0, 0, 255)            #*****◘******************************************************Modified y Sonda ******************cd l
            )
        dpg.bind_item_font(result, self.font2)

    def showQA(self, QA: QuestionAndAnswer):
        prompts = {
            "description": QA.description,
            "navigation": QA.navigation,
            "actions": QA.actions
        }
        response = QA.response
        self.showPrompts(prompts)
        self.showResponse(response)

    def render_loop(self):
        self.update_inertial_zoom()
        dpg.delete_item("Canvas", children_only=True)
        canvasNode = dpg.add_draw_node(parent="Canvas")
        try:
            roadgraphRenderData, VRDDict = self.renderQueue.get()
            egoVRD = VRDDict['egoCar'][0]
            ex = egoVRD.x
            ey = egoVRD.y
            self.drawRoadgraph(canvasNode, roadgraphRenderData, ex, ey)
            self.drawVehicles(canvasNode, VRDDict, ex, ey)
            # self.drawMovingSce(movingSceNode, egoVRD)
        except TypeError:
            return
        
        try:
            cameraImagesList = self.imageQueue.get(1)
            if cameraImagesList:
                self.showImage(cameraImagesList[0])
        except TypeError:
            return
        
        try:
            QA = self.QAQ.get()
            if QA:
                self.showQA(QA)
        except TypeError:
            return

    def run(self):
        self.setup()
        self.create_windows()
        self.create_handlers()
        self.resize_windows()
        self.ctf = CoordTF(120, 'BEVWindow')
        dpg.show_viewport()
        self.drawMainWindowWhiteBG()
        while dpg.is_dearpygui_running():
            self.render_loop()
            dpg.render_dearpygui_frame()
