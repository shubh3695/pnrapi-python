import pnrapi
p = pnrapi.PnrApi("4255598107") #10-digit PNR Number
if p.request() == True:
    print p.get_json()
else:
    print p.error

