from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from urx import robot as urx
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

global robot
robot = None

def initRobot(request, ip):
    global robot
    # return HttpResponse(ip)
    try:
        robot = urx.URRobot(ip)
        robot.set_payload(0.35, (0, 0, 0))

        # robot.set_tcp((0, 0, 0.151, 0, 0, 0))
        # TPC ( (PositionX, PositionY, PositionZ, OrientationRX, OrientationRY, OrientationRZ) )
        robot.set_tcp((-0.7616, 0.078, 0.7086, 0, 0, 0))


        if robot.is_running():
            return JsonResponse({'status': 200, 'message': 'Poziția robotului: ' + str(robot.is_running())})
        else: 
            raise Exception("Error initializing robot")
    except Exception as e:
        return JsonResponse({'status': 400, 'message': 'Poziția robotului: ' + str(robot.is_running()), 'errorMessage':  str(e)})
    

def getPosition(request):
    global robot

    robotPos = robot.getl()

    print(robotPos)

    return HttpResponse(robotPos)   

def moveInitialPosition(request):
    global robot

    init_pose= [0.600525622392412, -0.23278915712382445, -0.3322044984512897, -0.04176787055215222, -3.138968824031173, -0.010858511312736064]

    robot.movel(init_pose, acc=0.1, vel=0.1)

    return HttpResponse("Robot moved to initial position")

@require_POST
@csrf_exempt  # Add this decorator to exempt the view from CSRF checks
def movePosition(request):
    global robot
# $body = '[{"position": [0.600525622392412, -0.23278915712382445, -0.3322044984512897, -0.04176787055215222, -3.138968824031173, -0.010858511312736064]}]'  Invoke-WebRequest -Uri "http://127.0.0.1:8000/robot/movePosition/" -Method POST -Body $body -ContentType "application/json"

    try:
        data = json.loads(request.body)

        if isinstance(data, dict):
            positions_processed = []
            for obj in data:
                # Assuming 'obj' has a 'position' field to process
                position = obj.get('position')
                # Simulate processing the position. Replace with actual robot movement logic.
                # robot.move_to(position)
                positions_processed.append(position)

            nextMove = positions_processed[0].copy()
            
            print (positions_processed)
            robot.movel(nextMove, acc=0.1, vel=0.1) # Move to the first position in the list
            return JsonResponse({'status': 'success', 'message': 'All positions processed.', 'positions': nextMove})
        else:
            return JsonResponse({'status': 'error', 'message': 'Expected a list of objects.'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)