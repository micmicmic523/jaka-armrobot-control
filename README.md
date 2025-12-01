# jaka-armrobot-control
Python-based control interface for 6-axis Jaka Robot using TCP Socket and Multiprocessing for real-time communication.

## 📱 System Integration
This Python script acts as the **Backend Control Server** for the Jaka Arm Robot.

**How it works:**
1.  The Mobile App sends an integer code (e.g., `1`, `2`, `3`) via TCP Socket.
2.  This Python script receives the code and processes it using a **State Machine** logic.
3.  The script executes the corresponding robot trajectory using `multiprocessing` to prevent blocking the network thread.
4.  Feedback is sent back to the App to update the UI status.

[ Mobile App ]  ---> (TCP Socket) ---> [ Python Backend (This Repo) ] ---> [ Jaka Robot Controller ]

> *Note: This repository contains the Backend/Control logic. The mobile application frontend is documented separately.*
