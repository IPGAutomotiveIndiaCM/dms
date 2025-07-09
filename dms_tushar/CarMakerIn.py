import sys
sys.path.append("C:/IPG/carmaker/win64-14.0.1/Python/python3.9")
import cmapi
import pathlib
import subprocess
from cmapi import SimControlInteractive
#import movienxapi
from cmapi import time, Runtime, Project, Variation, Application, AppType, ApoServer
#cmapi.logger.setLevel("DEBUG")
kpit_sc = cmapi.SimControlInteractive()
 
async def start_gui():
    print("GUI OPEN")
    subprocess.Popen([r"C:\IPG\carmaker\win64-14.0.1\bin\CM_Office.exe"]+ ["-connect"])
 
   
async def start_movies():
    movie = Application.create(cmapi.AppType.IPGMovie)
    movie.set_executable_path("C:/IPG/carmaker/win64-14.0.1/GUI/Movie.exe")
    movie.set_arg("-apphost", "localhost")
    await movie.start()
 
 
async def main():
 
    project_path = pathlib.Path(r"D:\Office\CM_Projects\CM13\Bhoomika")
    cmapi.Project.load(project_path)
 
    testrun_path = pathlib.Path(r"D:\Office\CM_Projects\CM13\Bhoomika\Data\TestRun\Overtaking")
    testrun = cmapi.Project.instance().load_testrun_parametrization(testrun_path)
   
    variation = cmapi.Variation.create_from_testrun(testrun.clone())
    variation.set_name("KPIT_Variation")
 
    print("now we added variation")
    cmapi.logger.info("now we added variation")
 
   
    variation.set_initial_realtimefactor(1)
 
   
    kpit_sc.set_variation(variation)
 
   # await cmapi.Task.run_task_bg(start_gui())
   
 
    master = cmapi.CarMaker()
    await kpit_sc.set_master(master)
    print("master connected")
 
    await cmapi.Task.run_task_bg(start_gui())
    await cmapi.Task.run_task_bg(start_movies())
 
    await kpit_sc.start_and_connect()
    print ("start and connect happened")
 
 
    await cmapi.Task.sleep(20)
 
   
    await kpit_sc.start_sim()
    print ("started")
    await kpit_sc.create_rtexpr_condition("Time > 10").wait()
    # Trigger DVA Write command for 5000ms:
    kpit_sc.simio.dva_write_absolute_value(name="VC.Brake", value=0.12345, duration=5000)
    await kpit_sc.create_simstate_condition(cmapi.ConditionSimState.finished).wait()
 
    await kpit_sc.stop_and_disconnect()
    print("stopped")    
   
 
if __name__ == "__main__":
    cmapi.Task.run_main_task(main())