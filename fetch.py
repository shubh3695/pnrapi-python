import pnrapi
p = pnrapi.PnrApi("2350323124") #10-digit PNR Number
if p.request() == True:
    print p.get_json()
else:
    print p.error

