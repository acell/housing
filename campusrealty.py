from geopy.geocoders import Nominatim
from lxml import html

import json
import requests

geolocator = Nominatim()

data = []
entry = {}
geojson = {}
counterStart = 0
counterMid = 0
counterMid1 = 0
counterMid2 = 0
counterMid3 = 0
counterMid4 = 0
counterEnd = 0
latloncount = 0
brim = 1

results = []
geojson["type"] = "FeatureCollection"

# CAMPUS REALTY

for x in range(0, 200):
    try:

        resultInfo = {}

        resultInfo["type"] = "Feature"

        entry = {}

        x = str(x)

        entry["id"] = x

        page = requests.get('http://www.campusrealty.com/view-unit.php?id=%s' % x)
        tree = html.fromstring(page.content)

        try:
            addressInfo = {}
            addressInfo["type"] = "Point"
            address = (tree.xpath('/html/body/div[3]/div/h2/text()'))

            try:
                index = address[0].index('#')
                address = str(address[0][:index]) + 'Avenue Ann Arbor'
            except:
                address = str(address[0]) + 'Avenue Ann Arbor'

            location = geolocator.geocode(address)

            if location == None:
                address = str(address[0][:index]) + ' Street Ann Arbor'
                location = geolocator.geocode(address)

            if location == None:
                address = str(address[0][:index]) + ' Road Ann Arbor'
                location = geolocator.geocode(address)

            if location == None:
                address = str(address[0][:index]) + ' Court Ann Arbor'
                location = geolocator.geocode(address)

            if location == None:
                address = str(address[0][:index]) + ' Blvd Ann Arbor'
                location = geolocator.geocode(address)

            if location == None:
                address = str(address[0][:index]) + ' Place Ann Arbor'
                location = geolocator.geocode(address)

            entry["address"] = address
            latlon = []
            latlon.append(location.longitude)
            latlon.append(location.latitude)
            addressInfo["coordinates"] = latlon
            latloncount += 1
            resultInfo["geometry"] = addressInfo
        except:
            addressInfo = {}
            addressInfo["type"] = "Point"
            addressInfo["coordinates"] = [-83.65, 42.25]
            resultInfo["geometry"] = addressInfo

        bedrooms = (tree.xpath('/html/body/div[3]/div/p[1]/text()[1]'))
        bedrooms = int(bedrooms[0])
        entry["bedrooms"] = bedrooms
        contact_link = ('http://www.campusrealty.com/view-unit.php?id=%s' % x)
        entry["contact"] = str(contact_link)
        counterStart += 1

        bathrooms = tree.xpath('/html/body/div[3]/div/p[1]/text()[3]')
        bathrooms = bathrooms[0]
        entry["bathrooms"] = bathrooms
        counterMid += 1

        try:
            totalRent = tree.xpath('/html/body/div[3]/div/p[1]/text()[7]')
            totalRent = totalRent[0]
            totalRent = totalRent[2:7]
            totalRent = totalRent.split(',')
            totalRent = float(totalRent[0] + totalRent[1])
            entry["totalRent"] = totalRent
            counterMid2 += 1
        except:
            totalRent = tree.xpath('/html/body/div[3]/div/p[1]/text()[7]')
            totalRent = totalRent[0]
            totalRent = totalRent[2:5]
            entry["totalRent"] = totalRent
            counterMid2 += 1

        rent = totalRent/bedrooms
        entry["rent"] = totalRent
        entry["rent_per_person"] = rent
        counterMid3 += 1

        data.append(entry)
        counterEnd += 1

        resultInfo["properties"] = entry

        resultInfo["type"] = "Feature"

        results.append(resultInfo)

    except:

        pass

# print(results)
# SHOW ME THE RENT

for y in range (0, 29):
    page = requests.get('https://www.showmetherent.com/listings/48104/sw:42.263193001547734,-83.75272457462711/ne:42.28811194675993,-83.71870432410333/start:%d' % (y * 20))
    for x in range(1, 20):
        tree = html.fromstring(page.content)
        address = str(tree.xpath('//*[@id="listing-list"]/div[1]/div[%d]/div[2]/h2/a/text()' % x))[2:-2]
        update_date = str(tree.xpath('//*[@id="listing-list"]/div[1]/div[%d]/div[3]/p[1]/text()' % x))
        bedrooms = str(tree.xpath('//*[@id="listing-list"]/div[1]/div[%d]/div[3]/p[2]/text()' % x))
        house_type = str(tree.xpath('//*[@id="listing-list"]/div[1]/div[%d]/div[3]/p[3]/text()' % x))
        lease_date = str(tree.xpath('//*[@id="listing-list"]/div[1]/div[%d]/div[4]/a/text()' % x))
        rent = str(tree.xpath('//*[@id="listing-list"]/div[1]/div[%d]/div[4]/p[1]/text()' % x))[2:-2]
        try:
            contact_link = "https://www.showmetherent.com" + str(tree.xpath('//*[@id="listing-list"]/div[1]/div[%d]/div[2]/h2/a/@href' % x))[2:-2]
        except:
            contact_link = "https://www.showmetherent.com"

        latlon = []
        location = ''
        entry = {}
        resultInfo = {}
        resultInfo["type"] = "Feature"

        addressInfo = {}
        addressInfo["type"] = "Point"

        try:
            location = geolocator.geocode(address + ' Ann Arbor')
            latlon.append(location.longitude)
            latlon.append(location.latitude)
            addressInfo["coordinates"] = latlon
            entry["rent"] = rent
            if(len(entry["rent"]) > 8):
                rent = rent.replace("$", "")
                rent = rent.replace(",", "")
                dash = rent.index("-")
                rent_low = rent[:(dash - 1)]
                rent_high = rent[(dash + 2):]
                entry["rent"] = rent_low
                entry["rent_high"] = rent_high
            else:
                rent = rent.replace(",", "")
                rent = rent.replace("$", "")
                entry["rent"] = rent
            entry["bedrooms"] = bedrooms
            if(len(entry["bedrooms"]) > 14):
                entry["bedrooms_low"] = bedrooms[2:3].replace(" ", "")
                entry["bedrooms_high"] = bedrooms[6:7].replace(" ", "")
                entry["bedrooms"] = bedrooms[2:3].replace(" ", "")
            else:
                entry["bedrooms"] = bedrooms[2:3].replace(" ", "")

            try:
                if (float(entry["rent"])/float(bedrooms[2])) > 350:
                    entry["rent_per_person"] = (float(entry["rent"])/float(bedrooms[2]))
                else:
                    entry["rent_per_person"] = float(entry["rent"])
            except:
                try:
                    entry["rent_per_person"] = float(entry["rent"])
                except:
                    entry["rent_per_person"] = 9999

            entry["address"] = address
            entry["type"] = "Feature"
            entry["house_type"] = house_type[2:]
            entry["lease_date"] = lease_date
            entry["update"] = update_date
            entry["contact"] = str(contact_link)
            resultInfo["geometry"] = addressInfo
            resultInfo["properties"] = entry
            resultInfo["updated"] = lease_date
            results.append(resultInfo)
        except:
            pass


# remove when editing
geojson["features"] = results
with open('housingsmtr.geojson', 'w') as outfile:
    json.dump(geojson, outfile)
