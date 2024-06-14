
import  jpype     
import  asposecells     
jpype.startJVM() 
from asposecells.api import Workbook


def converter(in_put, out_put):
    workbook = Workbook(in_put)
    workbook.save(out_put)
    jpype.shutdownJVM()
	
