from sightengine.client import SightengineClient

client = SightengineClient('82714170', 'RT4oo9fZFDbNsrvV6VSp')

checkNudity = client.check('nudity')

invalidImage = False

output = client.check('nudity', 'wad', 'celebrities', 'scam', 'face-attributes').set_file('C:/Users/rakes/Desktop/gal_gadot_nude-2.jpg')

# contains nudity
if output['nudity']['safe'] <= output['nudity']['partial'] and output['nudity']['safe'] <= output['nudity']['raw']:
    invalidImage = True
# contains weapon, alcohol or drugs
if output['weapon'] > 0.2 or output['alcohol'] > 0.2 or output['drugs'] > 0.2:
    invalidImage = True
# contains scammers
if output['scam']['prob'] > 0.85:
    invalidImage = True
# contains celebrities
if 'celebrity' in output:
    if output[0]['prob'] > 0.85:
        invalidImage = True
# contains children
if 'attributes' in output:
    if output['attributes']['minor'] > 0.85:
        invalidImage = True

# output2 = checkNudity.set_url('https://d3m9459r9kwism.cloudfront.net/img/examples/example5.jpg')

# assign binary_image
# output3 = checkNudity.set_bytes('C:/Users/rakes/Desktop/gal_gadot_nude-2.jpg')

print(invalidImage)
# print(output2)
# print(output3)

####### check video

check = client.check('nudity', 'wad')
output = check.video('https://sightengine.com/assets/stream/examples/funfair.mp4', 'http://requestb.in/1nm1vw11')

output2 = check.video_sync('https://sightengine.com/assets/stream/examples/funfair.mp4')

# print(output)
# print(output2)
