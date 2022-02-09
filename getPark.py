# -*- coding:utf-8 -*-  
import csv
import requests
import json
import time
import math

#name+location
def get_LocationName(path):           
    with open(path,'r') as f:
        reader = csv.reader(f)
        tem_list_locations = [row[0] for row in reader]
        #print(tem_list_locations)
        #print(len(tem_list_locations))
        while '' in tem_list_locations:
            tem_list_locations.remove('')
        #print(tem_list_locations)
        #print(len(tem_list_locations))
    with open(path,'r') as f:
        reader = csv.reader(f)    
        tem_list_details = [row[13] for row in reader]
        while '' in tem_list_details:
            tem_list_details.remove('')
        #print(len(tem_list_details))
    #print(tem_list_locations)
    #print(tem_list_details)
    list_locations = []
    for i in range(len(tem_list_locations)):
        if i > 0:
            list_locations.append(tem_list_locations[i] + tem_list_details[i])
    #print(list_locations)
    return list_locations
    #print('done')
 
# #name   
# def get_LocationName(path):           
#     with open(path,'r') as f:
#         reader = csv.reader(f)
#         tem_list_locations = [row[0] for row in reader]
#         #print(tem_list_locations)
#         #print(len(tem_list_locations))
#         while '' in tem_list_locations:
#             tem_list_locations.remove('')
#         #print(tem_list_locations)
#         #print(len(tem_list_locations))
#     list_locations = []
#     for i in range(len(tem_list_locations)):
#         if i > 0:
#             list_locations.append(tem_list_locations[i])
#     #print(list_locations)
#     return list_locations
#     #print('done')
   
def getLat_Lng(list_locations,ak):
    list_o_location = []
    count = 0
    for locations in list_locations:
        if locations == "":
            break
        else:
            count = count +1
            print(count)
            url = "http://api.map.baidu.com/geocoder/v2/?address=" + locations + "&output=json&ak=" + ak
            #print(url)
            r = requests.get(url)
            data = r.json()
            results = data['result']
            lng = results['location']['lng']
            lat = results['location']['lat']
            precise = results['precise']
            confidence = results['confidence']
            level = results['level']
            latlng = [str(lat),str(lng)]
            list_o_location.append(latlng)
    return list_o_location     

def get_everything(results,o_location,pt_path,ak):
    name_list = []
    addre_list = []
    lat_list = []
    lng_list = []
    for result in results:
        jname = result['name']
        jlat = result['location']['lat']
        jlng = result['location']['lng']
        name_list.append(jname)
        lat_list.append(jlat)
        lng_list.append(jlng)
    #print(name_list)
#     print(lat_list)
#     print(lng_list)
#     print(addre_list)
    #
    power_list = []
    flow_list = []
    loca_list = []
    dist_list = []
    orient_list = []
    #
    #print(flow_list)
    #print('flow down')
    #
    for i in range(len(lat_list)):
        lat_lng = str(lat_list[i]) + ',' + str(lng_list[i])
        loca_list.append(lat_lng)
    for loca in loca_list:
        dist_url = 'http://api.map.baidu.com/routematrix/v2/walking?output=json&origins=' + loca + '&destinations=' + str(o_location[0])+ ',' + str(o_location[1]) + '&ak=' + ak
        r = requests.get(dist_url)
        #print(r)
        dist_data = r.json()
        #print(dist_data)
        dist = dist_data['result'][0]['distance']['value']
        dist_list.append(dist)

    #print(dist_list)
    #print('distance done')
    #
    for i in range(len(loca_list)):
        start_point = [lat_list[i],lng_list[i]]
        se_arc = getDistance(start_point , o_location)
        orient_list.append(se_arc)
    #print(orient_list)
    #print('orientation done')
    #
    power1 = 0
    power2 = 0
    power3 = 0
    power4 = 0
    power5 = 0
    power6 = 0
    power7 = 0
    power8 = 0
    for i in range(len(loca_list)):
        if dist_list[i] > 0:
            if orient_list[i] == 1:
                power1 = power1 + 1000/float(dist_list[i])
            elif orient_list[i] == 2:
                power2 = power2 + 1000/float(dist_list[i])
            elif orient_list[i] == 3:
                power3 = power3 + 1000/float(dist_list[i])
            elif orient_list[i] == 4:
                power4 = power4 + 1000/float(dist_list[i])
            elif orient_list[i] == 5:
                power5 = power5 + 1000/float(dist_list[i])
            elif orient_list[i] == 6:
                power6 = power6 + 1000/float(dist_list[i])
            elif orient_list[i] == 7:
                power7 = power7 + 1000/float(dist_list[i])
            else:
                power8 = power8 + 1000/float(dist_list[i])
    
    
    public_transportation = []
    public_transportation = [power1,power2,power3,power4,power5,power6,power7,power8]
    #print(public_transportation)
    return public_transportation


    

def getDistance(start_point,o_location):
    #
    o_location_lat = float(o_location[0])
    o_location_lng = float(o_location[1])
    #
    lat3 = (math.pi/180)*o_location_lat
    lon3 = (math.pi/180)*start_point[1]
    #
    lat1 = (math.pi/180)*start_point[0]  
    lat2 = (math.pi/180)*o_location_lat
    lon1 = (math.pi/180)*start_point[1]  
    lon2 = (math.pi/180)*o_location_lng 
    earth_R = 6371  
    dist_12 = math.acos(math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1))*earth_R
    dist_13 = math.acos(math.sin(lat1)*math.sin(lat3)+math.cos(lat1)*math.cos(lat3)*math.cos(lon3-lon1))*earth_R
    if dist_12 == 0:
        arc_12 =0
    else:
        arc_12 = math.acos(dist_13/dist_12)/math.pi*180
    if start_point[0] >= o_location_lat and start_point[1] >= o_location_lng :
        arc = int(arc_12)
    elif start_point[0] >= o_location_lat and start_point[1] <= o_location_lng :
        arc = int(180 - arc_12)
    elif start_point[0] <= o_location_lat and start_point[1] <= o_location_lng :
        arc = int(180 + arc_12)
    else:
        arc = int(360 - arc_12)
    arc_raw = arc
    if arc_raw >=315 and arc_raw < 360 :
        arcf = 1
    elif arc_raw >=270 and arc_raw < 315 :
        arcf = 2
    elif arc_raw >=225 and arc_raw < 270 :
        arcf = 3
    elif arc_raw >=180 and arc_raw < 225 :
        arcf = 4
    elif arc_raw >=135 and arc_raw < 180 :
        arcf = 5
    elif arc_raw >=90 and arc_raw < 135 :
        arcf = 6
    elif arc_raw>=45 and arc_raw < 90 :
        arcf = 7
    else:
        arcf = 8
    return arcf

def main():
    path = r'E:\MachineLearning-data\BusStation\2015library_list.csv' 
    ak = ["bpRD3CpFwDfyycnbxoc2LGHOGwTwtgGa","ZndtNzsyWVVKQ9ymwUYYmAKTjWCcxH1N","jvdszNo0PMWXKSEoX52q6DGhqb50c01X","9XlkpZhO3oQl2KebYe2rRQCsiCzTZBlt"]
    building_type = ['公交站','地铁站','公园','广场']
    t_type = building_type[3]
    list_locations = get_LocationName(path)
    #every_round = 5
    every_round = int(len(list_locations)/4)
    print(len(list_locations))
    if len(list_locations)%every_round == 0:
        total_round =len(list_locations)/every_round
    else:
        total_round = len(list_locations)//every_round + 1
    print(total_round)
    for i in range(int(total_round)):
        if every_round*(i+1)-1 >= len(list_locations):
            list_o_location = getLat_Lng(list_locations[every_round*i:len(list_locations)+1],ak[0])
        if every_round*(i+1)-1 < len(list_locations):
            list_o_location = getLat_Lng(list_locations[every_round*i:every_round*(i+1)],ak[0])
            #print(o_location)
        pt_path = "E:\\" + t_type + str(i+1) + ".csv"
        radius = 1000
        count = every_round*i
        public_transportation = []
        for o_location in list_o_location:
            count = count+1
            lona = list_locations[count-1]
            #print(o_location)
            url = "http://api.map.baidu.com/place/v2/search?query=" + t_type + "&tag=旅游景点&location=" + str(o_location[0])+ ',' + str(o_location[1]) + "&radius=" + str(radius) + "&output=json&sort_name:distance|sort_rule:1&ak=" + ak[0]
            #print(url)
            r = requests.get(url)
            #print(r)
            data = r.json()
            #print(data)
            results = data['results']
            #print(results)
            if results == []:
                public_transportation_addname = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                public_transportation_addname.insert(0, lona)
                public_transportation.append(public_transportation_addname)
            else :
                public_transportation_addname = get_everything(results,o_location,pt_path,ak[0])
                public_transportation_addname.insert(0, lona)
                public_transportation.append(public_transportation_addname)
            #print(public_transportation)
            print("done" + str(count))
        
        with open(pt_path,'w',newline='') as pt:
            writer = csv.writer(pt)
            #print(public_transportation)
            n = len(public_transportation)
            for i in range(n):
                writer.writerow(public_transportation[i])   
        print('sleeping')
        time.sleep(60)        
        print('start')
        
main()
print('done!!!')
    
    
