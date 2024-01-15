from time import sleep

from ev3dev2.motor import MediumMotor , LargeMotor, OUTPUT_A,OUTPUT_B, OUTPUT_D

from math import sqrt

from pixycamev3.pixy2 import Pixy2

class Robot(): 

    def __init__(self):
        
        # Initialize Pixy2 camera, motors
        self.pixy2 = Pixy2(port=1, i2c_address=0x54)
        self.motor_forward = LargeMotor(OUTPUT_A)
        self.motor_tilt = LargeMotor(OUTPUT_B)
        self.motor_shoot = MediumMotor(OUTPUT_D)

        # Store starting positions of motors
        self.motor_forward_starting_position = self.motor_forward.position
        self.motor_tilt_starting_position =  self.motor_tilt.position


        # Initialize variables for state tracking
        self.sequence=[-1,-1,-1,-1,1,1,1,1,1,1,1,1,2,-1,-1,-1,-1,-1,-1,-1,
                       -1,2,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-2,1,1
                       ,1,1,1,1,1,1,-2,-1,-1,-1,-1]
        
        self.indx_sequence = 0
        
        self.compt = 0
        self.comptx = 0
        self.compty = 0
        self.compt_dist = 0
        self.compute_dist = False
        self.bb_box = []
        self.pos_on_x = False
        self.pos_on_y = False
        self.loose_target = False
        self.compt_loss = 0 
        self.shoot = False
        self.distance = 0
        self.try_detect_target = True
        self.Align = False
        self.final_report = []
        self.left_ammo = 7
        self.is_running = True

        #Led switch on and off to show init is finish
        self.pixy2.set_lamp(1, 0)
        sleep(0.5)
        self.pixy2.set_lamp(0, 0)

    def output_information(self):
        if self.compute_dist:
            statu = "Shooting"        
        elif self.Align:
            statu = "Aligning"
        elif self.compute_dist:
            statu = "Computing distance"
        elif self.compt_loss > 0 :
            statu = "Looking for the lost Target"
        else : 
            statu = "Scanning"

        print("-"*20)
        print("Robot is " + statu)

    #Reboot function 
    def reboot(self) : 
        self.motor_forward.on_to_position(15, self.motor_forward_starting_position)
        self.motor_tilt.on_to_position(15, self.motor_tilt_starting_position)
        self.motor_forward.wait_while('running')
        self.motor_tilt.wait_while('running')
        self.indx_sequence = 0

    #Align camera on target funtion
    def align_camera_on_target(self,x,y) :

        #Case where the target is at the left of the image
        if x < 148 : 
            angle_x = 30 - (x/158 * 30)
            self.motor_forward.on_for_degrees(speed=15, degrees=angle_x* 2.5)
            self.motor_forward.wait_while('running')
            self.compt = 0
        #Case where the target is at the right of the image
        elif x > 168 :
            angle_x =  -((x-158)/158 * 30) 
            self.motor_forward.on_for_degrees(speed=15, degrees=angle_x* 2.5)
            self.motor_forward.wait_while('running')        
            self.compt = 0
        #Consider the target is align on the x axis
        else : 
            self.pos_on_x = True

        print(y)
        #Case where the target is at the bottom of the image
        if y < 94 : 
            angle_y = 20 - (y/104 * 20)
            self.motor_tilt.on_for_degrees(6,angle_y)
            self.motor_tilt.wait_while('running')
            self.compt = 0
        #Case where the target is at the top of the image
        elif y > 114 :
            angle_y =  -((y-104)/104 * 20) 
            self.motor_tilt.on_for_degrees(6,angle_y)
            self.motor_tilt.wait_while('running')  
            self.compt = 0    
        else :
            self.pos_on_y = True

        #Consider the target is align with the camera
        if self.pos_on_x and self.pos_on_y : 
            self.compt += 1

        #For the number of frame the camera and the target have been align, we can go the other phase
        if self.compt >= 5 : 
            self.Align = False
            self.compute_dist = True
            self.compt = 0

    def compute_distance_target(self,w,h) :

        #We have get bbox values for x frames and can compute
        if self.compt_dist >= 15 : 
            average_w, average_h = map(lambda z: sum(z) / len(self.bb_box), zip(*self.bb_box))

            #Pythagore and rule of 3 to estimate the distance
            average_diag = sqrt((average_w**2) + (average_h**2))

            self.distance = (378*0.16) / average_diag
            self.compute_dist = False  
            self.shoot = True            
            self.bb_box = []
            self.compt_dist = 0
        else : 
            self.bb_box.append([w,h])
            self.compt_dist += 1

    def shooting_sequence(self):

        #We compute the angle to add determine by our equation
        reglage_angle = 3.74 + (0.06*(self.motor_tilt.position - self.motor_tilt_starting_position))  + (13.37*self.distance)

        #Apply the angle and shoot 
        self.motor_tilt.on_for_degrees(10,reglage_angle)
        self.motor_shoot.on_for_degrees(speed=23, degrees=-380)
        self.motor_shoot.wait_while('running')

        self.motor_shoot.on_for_degrees(speed=23, degrees=380)
        self.motor_shoot.wait_while('running')
        
        self.output_shooting_information(reglage_angle)
        self.reboot()
        self.shoot = False
        self.try_detect_target = True 

        if self.left_ammo == 0:
            self.is_running = False

    def output_shooting_information(self, reglage_angle):

        report = ("-"*20) + "\n"
        report = report +"Cordinate about the target : " + str(self.motor_forward.position - self.motor_forward_starting_position)
        report = report + " " + str(self.motor_tilt.position - self.motor_tilt_starting_position)
        report = report + "\n" + "Distance : " + str(self.distance)
        report = report + "\n" + "Shooting angle : " + str(reglage_angle)
        report = report + "\n" + "Ammo left : " + str(self.left_ammo)
        
        self.final_report.append(report)

        with open('final_report.txt', 'w') as file:
            for item in self.final_report:
                file.write("%s\n" % item)

        print(report)


    def loose_target_verification(self) : 

        #The target have been lost for x frame so we reboot the system
        if self.compt_loss >= 5 : 
            self.loose_target = False
            self.reboot
            self.compt_loss = 0 
            self.Align = False
            self.try_detect_target = True
        else :
            self.compt_loss += 1 

    def scanning_sequence(self): 


        #Apply the sequence of scan 
        move = self.sequence[self.indx_sequence]
        if move == 1 : 
            self.motor_forward.on_for_degrees(speed=15, degrees=30 * 2.5)
            self.motor_forward.wait_while('running')
        elif move == -1 : 
            self.motor_forward.on_for_degrees(speed=15, degrees=-30 * 2.5)
            self.motor_forward.wait_while('running')
        elif move == 2 : 
            self.motor_tilt.on_for_degrees(10,27)
            self.motor_tilt.wait_while('running')
        elif move == -2 : 
            self.motor_tilt.on_for_degrees(10,-27)
            self.motor_tilt.wait_while('running')
        self.indx_sequence += 1 
        #We arrive at the starting point of the sequence so reset the index
        if self.indx_sequence ==len(self.sequence) : 

            self.indx_sequence = 0 


    def main(self):

        while self.is_running :
            nbr , target = self.pixy2.get_blocks(1,1)
            if nbr >= 1 :
                self.loose_target = True
                if self.try_detect_target : 
                    self.Align = True
                    self.try_detect_target = False

                x = target[0].x_center
                y = target[0].y_center
                w = target[0].width
                h = target[0].height

                if self.Align :

                    self.align_camera_on_target(x,y)

                if self.compute_dist :

                    self.compute_distance_target(w,h)

                if self.shoot : 

                    self.shooting_sequence()


            elif self.loose_target :

                self.loose_target_verification()

            else : 
                
                self.scanning_sequence()

            self.output_information()

        ready = input("Press enter when the reload is done : ")
        self.is_running = True
        self.main()
            
robot = Robot()

robot.main()