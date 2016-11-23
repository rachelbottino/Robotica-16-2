#!/usr/bin/env python

import roslib; roslib.load_manifest('smach_tutorials')
import rospy
import smach
import smach_ros

x = 0
y = 0
z = 0 
id = 0

x_desejado = 0.12
y_desejado = 0.10
z_desejado = 1.80

def recebe(msg):
    global x
    global y
    global z
    global id
    for marker in msg.markers:
        x = round(marker.pose.pose.position.x, 2)
        y = round(marker.pose.pose.position.y, 2)
        z = round(marker.pose.pose.position.z, 2)
        #print(x)
        id = marker.id

# define state Foo
class Longe(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['ainda_longe','perto'])
        self.counter = 0

    def execute(self, userdata):
        global velocidade_saida
        rospy.loginfo('Executing state LONGE')
        if x > x_desejado:
            return 'ainda_longe'
        else:
            vel = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
            velocidade_saida.publish(vel)
            return 'perto'


# define state Bar
class Andando(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['ainda_longe'])

    def execute(self, userdata):
        global velocidade_saida
        rospy.loginfo('Executing state ANDANDO')
        #comando para andar
        vel = Twist(Vector3(0.5, 0, 0), Vector3(0, 0, 0))
        velocidade_saida.publish(vel)
        #rospy.sleep(0.05)

        return 'ainda_longe'
        



# main
def main():
    global velocidade_saida
    rospy.init_node('smach_example_state_machine')
    recebedor = rospy.Subscriber("/ar_pose_marker", AlvarMarkers, recebe)
    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['terminei'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('LONGE', Longe(), 
                               transitions={'ainda_longe':'ANDANDO', 
                                            'perto':'terminei'})
        smach.StateMachine.add('ANDANDO', Andando(), 
                               transitions={'ainda_longe':'LONGE'})

    # Execute SMACH plan
    outcome = sm.execute()


if __name__ == '__main__':
    main()
