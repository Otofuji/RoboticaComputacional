#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#Every Python ROS Node will have this declaration at the top.
#The first line makes sure your script is executed as a Python script

#####################################################################

#                           The Code Explained

#####################################################################


import rospy
# We need to import rospy if we are writing a ROS Node
from nav_msgs.msg import Odometry
# The nav_msgs/Odometry message stores an estimate of... 
# ...the position and velocity of a robot in free space:
from geometry_msgs.msg import Twist
# The cmd_vel message is of type geometry_msgs/Twist.
from math import fabs
from sensor_msgs.msg import LaserScan

velocidade_objetivo = Twist()
#Twist e uma classe

velocidade = 0

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=3)
#publisher('talker') node continually broadcast a message.

def notificacao(data):
    """
        Codigo de notificacao executado sempre que chega uma leitura da odometria

        Esta leitura chega na variavel data e e'  um objeto do tipo odometria
    """
    # Todo: a partir de uma leitura da odometria faça
    # um publish na velocidade até que o robô tenha andado 2 metros
    print("passei  em notificacao")



def trataLaser(data):
   
    global velocidade
   

    print("passei pelo trataLaser")

    media = sum(data.ranges[0:11])/len(data.ranges[0:11])

    print("Media de 0 a 10 ", media)
    print(data.ranges[3])
    if media <= 0.2:
        media = 0

    velocidade = 0.25*data.ranges[3]
    print("Velocidade: ", velocidade)
"""    velocidade_objetivo = Twist()
    velocidade_objetivo.linear.x = 1
    velocidade_objetivo.linear.y = 0
    velocidade_objetivo.linear.z = 0
    velocidade_objetivo.angular.z = 0"""

    #pub.publish(velocidade_objetivo)
       




def controle():
    """
        Função inicial do programa
    """
    rospy.init_node('Exemplo_Python')
    '''
    velocidade_objetivo = Twist()
    velocidade_objetivo.linear.x = 10
    velocidade_objetivo.linear.y = 0
    velocidade_objetivo.linear.z = 0
    velocidade_objetivo.angular.z = 10
    '''
    #However, our robot can't drive sideways (linear.y), ...
    # ..or rotate about the x-axis!
    # ..Therefore, we will only be using linear.x and angular.z 
    #to control our robot.
    rospy.Subscriber('/odom', Odometry, notificacao)
    rospy.Subscriber('/scan', LaserScan, trataLaser)

    # Initial movement.    
    #pub.publish(velocidade_objetivo)
    print("passei em controle")
    #rospy.spin() # Faz um loop infinito para o ROS nao retornar
#print(controle())

if __name__ == '__main__':
    try:
        controle()
        
        while not rospy.is_shutdown():
            velocidade_objetivo = Twist()
            velocidade_objetivo.linear.x = velocidade
            velocidade_objetivo.linear.y = 0
            velocidade_objetivo.linear.z = 0
            velocidade_objetivo.angular.z = 0

            pub.publish(velocidade_objetivo)
            print("Velocidade while", velocidade)
            rospy.sleep(0.1)
        


    except rospy.ROSInterruptException:
        pass
