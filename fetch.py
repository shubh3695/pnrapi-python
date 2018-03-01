import pnrapi
p = pnrapi.PnrApi("8242343456") #10-digit PNR Number
if p.request() == True:
    print (p.get_json())
else:
    print (p.error)