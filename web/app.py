#
# from flask_restful import Resource, fields, marshal_with, marshal
# import datetime
#
#
#
# resource_fields = {
#     'name': fields.String,
#     'address': fields.String,
#     'date_upated': fields.DateTime(dt_format='rfc822')
# }
#
# class UserInfo(object):
#     def __init__(self, name, address, date_updated=datetime.now()):
#         self.name = name
#         self.address = address
#         self.date_updated = date_updated
#
# print(json.dumps(marshal(UserInfo('magi', 'beijing'), resource_fields))
#
from time import sleep
#
progress = 0

def testTime():
    # min = 00
    global progress
    sec = 0
    while 1==1:
        sleep(1)
        sec = sec + 1
        if (sec % 72 == 0):
            progress = int(sec / 72)
            # print(progress)
        print(sec)


testTime()
print(progress)



            # print(progress)
        # if (sec < 0):
        #     sec = 59
        #     # min = min - 1
        # if (min == 0):
        #     break
        # if (sec >=10 ):
        #     print(min,sec,sep=':')
        # if (sec <10 ):
        #     print(min, sec, sep=':0')
        # times = str(min) + ':' + str(sec)
        # print(sec)
#
print(testTime(0))
