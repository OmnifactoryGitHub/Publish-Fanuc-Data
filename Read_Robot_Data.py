import csv
from src.fanucpy.robot import Robot

class FanucReader:

    def get_next_reading(self):
        return {
            "power" : None,
            "X"     : None,
            "Y"     : None,
            "Z"     : None,
            "W"     : None,
            "P"     : None,
            "R"     : None,
            "J1"    : None,
            "J2"    : None,
            "J3"    : None, 
            "J4"    : None, 
            "J5"    : None, 
            "J6"    : None,
            "rdo"   : None, # The following are true if the value is 1, Gripper Open
            "rdi101": None, # Air Pressure On
            "rdi102": None, # Upper Beam Present
            "rdi103": None, # Lower Beam Present
            "rdi104": None, # Aerostructure Present
            "rdi105": None, # Upper Beam Stored
            "rdi106": None, # Lower Beam Stored
            "rdi107": None, # Aerostructure Stored
            "rdi108": None, # Blade Stored
            "do101" : None, # Upper Clamp Open
            "do102" : None  # Lower Clamp Open
        }
# The rdo here represents the gripper status, i.e. rdo 7 
# which in this case represents gripper open, if 1 gripper is open, if 0 gripper is closed.

class FanucReaderCSV(FanucReader):

    def __init__(self, robot_log=None) -> None:
        filename = robot_log if robot_log else 'robot_log.csv' 
        mydict = []
        with open(filename, mode='r') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                mydict.append({
                    k: str(v) if k == 'timestamp' else float(v) for k,v in row.items()
                })
        infile.close()
        self.fanuc_py = mydict
        self._iter = 0


    def get_next_reading(self, reset=True):
        reading = {
            "power" : self.fanuc_py[self._iter]["power"],
            "X"     : self.fanuc_py[self._iter]["X"],
            "Y"     : self.fanuc_py[self._iter]["Y"],
            "Z"     : self.fanuc_py[self._iter]["Z"],
            "W"     : self.fanuc_py[self._iter]["W"],
            "P"     : self.fanuc_py[self._iter]["P"],
            "R"     : self.fanuc_py[self._iter]["R"],
            "J1"    : self.fanuc_py[self._iter]["J1"],
            "J2"    : self.fanuc_py[self._iter]["J2"],
            "J3"    : self.fanuc_py[self._iter]["J3"], 
            "J4"    : self.fanuc_py[self._iter]["J4"], 
            "J5"    : self.fanuc_py[self._iter]["J5"], 
            "J6"    : self.fanuc_py[self._iter]["J6"],
            "rdo"   : self.fanuc_py[self._iter]["rdo"],
            "rdi101": self.fanuc_py[self._iter]["rdi101"],
            "rdi102": self.fanuc_py[self._iter]["rdi102"],
            "rdi103": self.fanuc_py[self._iter]["rdi103"],
            "rdi104": self.fanuc_py[self._iter]["rdi104"],
            "rdi105": self.fanuc_py[self._iter]["rdi105"],
            "rdi106": self.fanuc_py[self._iter]["rdi106"],
            "rdi107": self.fanuc_py[self._iter]["rdi107"],
            "rdi108": self.fanuc_py[self._iter]["rdi108"],
            "do101" : self.fanuc_py[self._iter]["do101"],
            "do102": self.fanuc_py[self._iter]["do102"]
        }
        self._iter += 1
        
        # Reset if reached the maximum level
        if reset and self._iter >= len(self.fanuc_py):
            self._iter = 0

        return reading


class FanucReaderRPI(FanucReader):

    def __init__(self, 
                robot_model='Fanuc',
                host="192.168.0.109",
                port=18736,
                ee_DO_type="RDO",
                ee_DO_num=7) -> None:
        
        self.robot_model = robot_model
        self.host        = host
        self.port        = port
        self.ee_DO_type  = ee_DO_type
        self.ee_DO_num   = ee_DO_num

        self.robot = Robot(
            robot_model=self.robot_model,
            host=self.host,
            port=self.port,
            ee_DO_type=self.ee_DO_type,
            ee_DO_num= self.ee_DO_num,
        )

        self.robot.connect()
    

    def get_next_reading(self):
        power   = self.robot.get_ins_power()
        curpos  = self.robot.get_curpos()
        curjpos = self.robot.get_curjpos()
        rdo     = self.robot.get_rdo(self.ee_DO_num)
        rdi101  = self.robot.get_din(101)
        rdi102  = self.robot.get_din(102)
        rdi103  = self.robot.get_din(103)
        rdi104  = self.robot.get_din(104)
        rdi105  = self.robot.get_din(105)
        rdi106  = self.robot.get_din(106)
        rdi107  = self.robot.get_din(107)
        rdi108  = self.robot.get_din(108)
        do101   = self.robot.get_dout(101)
        do102   = self.robot.get_dout(102)

        print(curpos)




        reading = {
            **{"power": power},
            **{ k: v for k, v in zip(['X', 'Y', 'Z', 'W', 'P', 'R'], curpos) },
            **{ k: v for k, v in zip(['J1', 'J2', 'J3', 'J4', 'J5', 'J6'], curjpos) },
            **{ "rdo": rdo }, 
            **{ "rdi101": rdi101 },
            **{ "rdi102": rdi102 },
            **{ "rdi103": rdi103 },
            **{ "rdi104": rdi104 },
            **{ "rdi105": rdi105 },
            **{ "rdi106": rdi106 },
            **{ "rdi107": rdi107 },
            **{ "rdi108": rdi108 },
            **{ "do101": do101 },
            **{ "do102": do102 }

        }
        ##### work needs doing here
        
        return reading




