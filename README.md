# DMS

1.Connect the device to the computer via the CAN bus

2.import dms_python package to your catkin_workspace,e.g. /home/xxx/catkin_ws/src/dms_python

3.```  
    catkin_make
    ```

4.setup can ```  
    sudo bash ./setup_can.sh can0 500000
    ```

5.startup roscore

6.``` rosrun dms_python listerner.py``` 

7.``` rosrun dms_python talker.py``` 
