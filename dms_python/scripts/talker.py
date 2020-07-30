#!/usr/bin/env python
# license removed for brevity
import rospy
import can
from std_msgs.msg import String

fatigue_dict = {'1': '闭眼', '2': '打哈欠','3': '睁眼睡','4': '低头','5': '左顾右盼','6': '无人脸',
                '7': '打电话','8': '抽烟','9': '遮挡','10': '抬头','11': '安全带',}

def fatigue_warning(coding):
    return fatigue_dict[coding]

def binary_to_T(str):
    str_length = len(str)
    result = 0
    for i in range(str_length):
        result += int(str[i])*pow(2,str_length-1-i)
    return result

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    bus = can.Bus(interface='socketcan',
              channel='can0',
              receive_own_messages=True)

    message = can.Message(arbitration_id=123, is_extended_id=True,
                      data=[0x11, 0x22, 0x33])
    
    bus.send(message, timeout=0.2)

    while not rospy.is_shutdown():
        for msg in bus:
            if msg.arbitration_id == 1921:
                binary_num = "{:08b}".format(msg.data[0])[4:]
                coding = binary_to_T(binary_num)
                fatigue_info = fatigue_warning(str(coding))
                rospy.loginfo(fatigue_info)
                pub.publish(fatigue_info)
                rate.sleep()
    # for msg in bus:
    #     if msg.arbitration_id == 1921:
    #         binary_num = "{:08b}".format(msg.data[0])[4:]
    #         coding = binary_to_T(binary_num)
    #         fatigue_info = fatigue_warning(str(coding))
    #         rospy.loginfo(fatigue_info)
    #         pub.publish(fatigue_info)
    #         rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass