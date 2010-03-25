'''
Created on Mar 24, 2010

@author: Barthelemy Dagenais
'''
from multiprocessing.process import Process
from py4j.java_gateway import JavaGateway
import subprocess
import time
import unittest


def start_example_server():
    subprocess.call(["java", "-cp", "../../../../py4j-java/bin/", "py4j.examples.ExampleApplication"])
    
    
def start_example_app_process():
    # XXX DO NOT FORGET TO KILL THE PROCESS IF THE TEST DOES NOT SUCCEED
    p = Process(target=start_example_server)
    p.start()
    return p

class Test(unittest.TestCase):

    def setUp(self):
#        logger = logging.getLogger("py4j")
#        logger.setLevel(logging.DEBUG)
#        logger.addHandler(logging.StreamHandler())
        self.p = start_example_app_process()
        time.sleep(0.5)
        self.gateway = JavaGateway()
        
    def tearDown(self):
        self.p.terminate()
        print('Shutting Down Gateway')
        self.gateway.shutdown()
        
        time.sleep(0.5)
    
    def testArray(self):
        self.gateway.jvm.py4j.GatewayServer.turnLoggingOn()
        example = self.gateway.entry_point.getNewExample()
        array1 = example.getStringArray()
        array2 = example.getIntArray()
        self.assertEqual(3,len(array1))
        self.assertEqual(4,len(array2))
        
        self.assertEqual(u'333',array1[2])
        self.assertEqual(5,array2[1])
        
        array1[2] = 'aaa'
        array2[1] = 6
        self.assertEqual(u'aaa',array1[2])
        self.assertEqual(6,array2[1])
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()