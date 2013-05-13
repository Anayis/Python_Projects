''' Converter logic that converts time t in 0.1 second
, ex. t = 1 = 0.1 second converting into a proper format
of min:second:0.1second

Written by Yuttannt Suwansiri 12 May 2013'''

# time in 0.1 second
t = 600
''' multiplier to convert 60 seconds to 1 minute
and so on...'''
secMultiplier = int(t / 600)
''' convert every 60 secs, 120 secs to 1 min, 2 min 
repectively and so on...'''
if secMultiplier > 0:
   sec = (t - 600 * secMultiplier) / 10
   sec = int(sec)
   sec = str(se
else:
   sec = t / 10 
   sec = int(sec)
# converting time to centi second or 0.1 second
csec = t % 10
# converting time to minute
min = int(t / 600)

print "min", min, "second", sec, "csec",csec