# facial_recognition
The aim of our facial recognition project is to be implemented in an employee check-in system to enhance security and streamline the check-in process. 
Using facial recognition, employees can simply scan their faces at checkpoints to gain access/authorization to specific areas of the building. Thus, facial recognition provides a secure, convenient, and efficient solution for employees, improving workplace efficiency. 

This approach eliminates the need for physical keys and reduces the risk of unauthorized access.

The procedure commences with the loading and encoding of employee images from a designated file. In the event that an employee’s image is absent, there is an option to add it, or conversely, remove it if the employee has departed from the company.

Subsequently, the system is designed to detect the face, pinpoint its location, and assign the name of the individual. This process is accompanied by the calculation of a confidence level and a blur score.

Upon successful identification of the person, a green LED light is activated, signaling “Access Granted”. In contrast, if the identification is unsuccessful, a red LED light is illuminated, indicating “Access Denied”. This approach ensures a high level of security and efficiency in access control.
