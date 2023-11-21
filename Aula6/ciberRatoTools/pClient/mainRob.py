
import sys
from croblink import *
from math import *
import xml.etree.ElementTree as ET

CELLROWS=7
CELLCOLS=14

class MyRob(CRobLinkAngs):
    def __init__(self, rob_name, rob_id, angles, host):
        CRobLinkAngs.__init__(self, rob_name, rob_id, angles, host)

    # In this map the center of cell (i,j), (i in 0..6, j in 0..13) is mapped to labMap[i*2][j*2].
    # to know if there is a wall on top of cell(i,j) (i in 0..5), check if the value of labMap[i*2+1][j*2] is space or not
    def setMap(self, labMap):
        self.labMap = labMap

        self.last_error = 0

    def printMap(self):
        for l in reversed(self.labMap):
            print(''.join([str(l) for l in l]))

    def run(self):
        if self.status != 0:
            print("Connection refused or error")
            quit()

        state = 'stop'
        stopped_state = 'run'

        N = 100

        i = 0
        print("\nBang Bang Orientation Controller")
        while i < N:
            self.readSensors()
            self.BangBangOrientationController(pi/2)
            i += 1

        i = 0
        print("\nProportional Orientation Controller")
        while i < N:
            self.readSensors()
            self.ProportionalOrientationController(pi/2)
            i += 1

        i = 0
        print("\nProportional-Derivative Orientation Controller")
        while i < N:
            self.readSensors()
            self.ProportionalOrientationDerivativeController(pi/2)
            i += 1

        i = 0
        print("\nBang Bang Position Controller")
        while i < N:
            self.readSensors()
            self.BangBangPositionController([2, 2])
            i += 1

        i = 0
        print("\nProportional Position Controller")
        while i < N:
            self.readSensors()
            self.ProportionalPositionController([4, 4])
            i += 1

        i = 0
        print("\nProportional-Derivative Position Controller")
        while i < N:
            self.readSensors()
            self.ProportionalPositionDerivativeController([6, 6])
            i += 1


            # if self.measures.endLed:
            #     print(self.robName + " exiting")
            #     quit()

            # if state == 'stop' and self.measures.start:
            #     state = stopped_state

            # if state != 'stop' and self.measures.stop:
            #     stopped_state = state
            #     state = 'stop'

            # if state == 'run':
            #     if self.measures.visitingLed==True:
            #         state='wait'
            #     if self.measures.ground==0:
            #         self.setVisitingLed(True);
            #     self.wander()
            # elif state=='wait':
            #     self.setReturningLed(True)
            #     if self.measures.visitingLed==True:
            #         self.setVisitingLed(False)
            #     if self.measures.returningLed==True:
            #         state='return'
            #     self.driveMotors(0.0,0.0)
            # elif state=='return':
            #     if self.measures.visitingLed==True:
            #         self.setVisitingLed(False)
            #     if self.measures.returningLed==True:
            #         self.setReturningLed(False)
            #     self.wander()

    def BangBangOrientationController(self, angle):
        # estimate error
        error = angle - (self.measures.compass * 180 / pi)
        while error > pi:
            error -= 2*pi
        while error < -pi:
            error += 2*pi
        # estimate control signal
        if error > 0:
            u = 0.15
        elif error < 0:
            u = -0.15
        else:
            u = 0            
        # apply control  
        print("u:", u)
        self.driveMotors(-u, u)

    def ProportionalOrientationController(self, angle):
        # estimate error
        error = angle - (self.measures.compass * 180 / pi)
        while error > pi:
            error -= 2*pi
        while error < -pi:
            error += 2*pi
        # estimate control signal
        k = 1
        u = k * error           
        # apply control  
        print("u:", u)
        self.driveMotors(-u, u)

    def ProportionalOrientationDerivativeController(self, angle):
        # estimate error
        error = angle - (self.measures.compass * 180 / pi)
        while error > pi:
            error -= 2*pi
        while error < -pi:
            error += 2*pi
        # estimate control signal
        kp = 1
        kd = 0.1
        error_anticipation = error - self.last_error
        u = kp * error + kd * error_anticipation
        self.last_error = error
        # apply control  
        print("u:", u)
        self.driveMotors(-u, u)

    def BangBangPositionController(self, pos):
        # estimate error
        error = [pos[0] - self.measures.x, pos[1] - self.measures.y]
        error = self.measures.compass - atan2(error[1], error[0])*180/pi
        # estimate control signal
        if error > 0:
            u = 0.15
        elif error < 0:
            u = -0.15
        else:
            u = 0            
        # apply control  
        print("u:", u)
        self.driveMotors(0.1+0.005*u, 0.1-0.005*u)

    def ProportionalPositionController(self, pos):           
        # estimate error
        error = [pos[0] - self.measures.x, pos[1] - self.measures.y]
        error = self.measures.compass - atan2(error[1], error[0])*180/pi
        # estimate control signal
        k = 1
        u = k * error             
        # apply control  
        print("u:", u)
        self.driveMotors(0.1+0.005*u, 0.1-0.005*u)

    def ProportionalPositionDerivativeController(self, pos):
        # estimate error
        error = [pos[0] - self.measures.x, pos[1] - self.measures.y]
        error = self.measures.compass - atan2(error[1], error[0])*180/pi
        # estimate control signal
        kp = 1
        kd = 0.1
        error_anticipation = error - self.last_error
        u = kp * error + kd * error_anticipation       
        # apply control  
        print("u:", u)
        self.driveMotors(0.1+0.005*u, 0.1-0.005*u)





    def wander(self):
        center_id = 0
        left_id = 1
        right_id = 2
        back_id = 3
        if    self.measures.irSensor[center_id] > 5.0\
           or self.measures.irSensor[left_id]   > 5.0\
           or self.measures.irSensor[right_id]  > 5.0\
           or self.measures.irSensor[back_id]   > 5.0:
            print('Rotate left')
            self.driveMotors(-0.1,+0.1)
        elif self.measures.irSensor[left_id]> 2.7:
            print('Rotate slowly right')
            self.driveMotors(0.1,0.0)
        elif self.measures.irSensor[right_id]> 2.7:
            print('Rotate slowly left')
            self.driveMotors(0.0,0.1)
        else:
            print('Go')
            self.driveMotors(0.1,0.1)

class Map():
    def __init__(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        
        self.labMap = [[' '] * (CELLCOLS*2-1) for i in range(CELLROWS*2-1) ]
        i=1
        for child in root.iter('Row'):
           line=child.attrib['Pattern']
           row =int(child.attrib['Pos'])
           if row % 2 == 0:  # this line defines vertical lines
               for c in range(len(line)):
                   if (c+1) % 3 == 0:
                       if line[c] == '|':
                           self.labMap[row][(c+1)//3*2-1]='|'
                       else:
                           None
           else:  # this line defines horizontal lines
               for c in range(len(line)):
                   if c % 3 == 0:
                       if line[c] == '-':
                           self.labMap[row][c//3*2]='-'
                       else:
                           None
               
           i=i+1


rob_name = "pClient1"
host = "localhost"
pos = 1
mapc = None

for i in range(1, len(sys.argv),2):
    if (sys.argv[i] == "--host" or sys.argv[i] == "-h") and i != len(sys.argv) - 1:
        host = sys.argv[i + 1]
    elif (sys.argv[i] == "--pos" or sys.argv[i] == "-p") and i != len(sys.argv) - 1:
        pos = int(sys.argv[i + 1])
    elif (sys.argv[i] == "--robname" or sys.argv[i] == "-r") and i != len(sys.argv) - 1:
        rob_name = sys.argv[i + 1]
    elif (sys.argv[i] == "--map" or sys.argv[i] == "-m") and i != len(sys.argv) - 1:
        mapc = Map(sys.argv[i + 1])
    else:
        print("Unkown argument", sys.argv[i])
        quit()

if __name__ == '__main__':
    rob=MyRob(rob_name,pos,[0.0,60.0,-60.0,180.0],host)
    if mapc != None:
        rob.setMap(mapc.labMap)
        rob.printMap()
    
    rob.run()
