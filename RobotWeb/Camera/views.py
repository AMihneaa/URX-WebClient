from django.shortcuts import render
from django.http import HttpResponse
import pyrealsense2 as rs
import numpy as np
from django.core.cache import cache
import cv2 as cv
# Create your views here.
global pipeline
pipeline=None



def Configure(request):
    global pipeline

    try:
        # Încercați să recuperați configurația din cache
        # pipeline = cache.get('camera_config')
        
        # Dacă configurația nu există în cache, configurați camera și salvați configurația
        
        if not pipeline:
            print("Pipeline is Nonefuck")
            pipeline=rs.pipeline()
            pipeline = configCamera(pipeline)
            print("pritn pip: " ,pipeline)
            if pipeline:
                 # None to keep in cache without expiration
                status = "Configuration successful"
            else:
                status = "Configuration failed1"
         # If configuration is successful, return a success status
        else: 
         status = "Configuration successful2"
    except Exception as e:
        # If an error occurs, return a failure status with the error message
        status = "Configuration failed2"
    
    return HttpResponse(status)

def Capture(request):
    global pipeline
    print("Global :", pipeline)

    try:
        if pipeline:
            
            captureStream(pipeline)
            status = "Capture successful"

        else:
            status = "Camera not configured"
       
    except Exception as e:
        # If an error occurs, return a failure status with the error message
        status = "Configuration failed2"
    
    return HttpResponse(status)



def configCamera(pipeline: rs) -> rs:
    try:
        print("in try\n")
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                print("RGB Camera found\n")
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        # config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        print("Configurare camera reusita\n")
        # Start streaming
        pipeline.start(config)
        
    except Exception as e:
        print("Eroare camera: ", e)

    return pipeline




def captureStream(pipeline: rs) -> None:
    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    if not depth_frame or not color_frame:
        pass

    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=0.03), cv.COLORMAP_JET)

    depth_colormap_dim = depth_colormap.shape
    color_colormap_dim = color_image.shape

    # If depth and color resolutions are different, resize color image to match depth image for display
    if depth_colormap_dim != color_colormap_dim:
        resized_color_image = cv.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv.INTER_AREA)
        # images = np.hstack((resized_color_image, depth_colormap)) # Pentru a scoate imaginea color si cea cu depth
        images = resized_color_image # Pentru a scoate doar imaginea color
    else:
        # images = np.hstack((color_image, depth_colormap)) # Pentru a scoate imaginea color si cea cu depth
        images = color_image # Pentru a scoate doar imaginea color


    count = 0
    img_path = "./images/"
    img_name = f"image_{count}.jpg"

    img_path = "{}{}".format(img_path, img_name)
    cv.imwrite(f"./Camera/images/{img_name}", images)
    print(img_path)
    print("Imaginea a fost salvata",images)
    
  