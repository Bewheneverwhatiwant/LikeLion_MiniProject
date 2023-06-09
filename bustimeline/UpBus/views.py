import xml.etree.ElementTree as ET
from django.shortcuts import render
import urllib.parse
from .apicaller import APICaller

#수정!! 확인바람

def bus_list(request):

    # 버스 번호와 정류장 정보
    bus_numbers = [1303, 1117, 1150, 1005]
    bus_stops = ['외대사거리', '모현사거리', '기숙사', '도서관', '파란지붕']

    # 실시간 버스 위치 정보를 저장할 딕셔너리
    bus_locations_Down = APICaller(228000345) #하행 종점 | 외대.모현빌라
    bus_locations_Up = APICaller(228000349) #상행 종점 | 한국외대종점
    bus_locations_info = APICaller(228000352)
    print('------------------------API 호출 끝!---------------------------')
    
    downList1 = [[],[],[],[],[]]
    downList2 = []
    for idx, inList in enumerate(downList1):
        for bus in bus_numbers:
            if bus_locations_Down[str(bus)].get('location') == str(4 - idx):
                inList.append(bus)
    for idx, inList in enumerate(downList1):
        if idx == 1:
            continue
        downList2.append(inList)
    print('하행버스-정류장 리스트화 (변환 전)')
    print(downList1)
    print('하행버스-정류장 리스트화 (변환 후)')
    print(downList2)

    upList = [[],[],[],[],[]]
    for idx, inList in enumerate(upList):
        for bus in bus_numbers:
            if bus_locations_Up[str(bus)].get('location') == str(idx):
                inList.append(bus)
    print('상행버스-정류장 리스트화')
    print(upList)

    upInfo = sorted(bus_locations_info.items(), key=lambda x: int(x[1]['predict_time']))
    print('정렬된 남은 버스 시간표')
    print(upInfo)

    
    

    context = {
        'bus_numbers': bus_numbers,
        'bus_stops': bus_stops,
        'downList' : downList1,
        'upList' : upList,
        'downListExist' : listChk(downList1),
        'upListExist' : listChk(upList),
        'busExist' : (listChk(downList1) or listChk(upList)),
        'upInfo' : upInfo,
    }

    return render(request, 'bus_list.html', context)

def listChk(chkList):
    listExist = 0
    for list in chkList:
        if list:
            listExist = 1
            break
    return listExist