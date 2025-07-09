loop =0

def create_brake_message():
    global loop
    loop +=1
    if loop <= 1:
        return  "DM.Lights.Hazard 1"
    if loop == 2:
        return  "LatCtrl.LKAS.SwitchedOn 1"
    if loop == 3:
        return "DM.Brake 1"
