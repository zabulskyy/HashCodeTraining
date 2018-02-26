import random
import math

golden = (1 + 5**0.5) / 2
maxloss = 100000

print("Reading")


class Video:
    def __init__(self, iid):
        self.iid = iid
        self.capacity = -1


class Server:
    def __init__(self, iid):
        self.iid = iid
        self.capacity = -1
        self.videos = []
        self.candidates = {}
        self.endpoints = []


class Endpoint:
    def __init__(self, iid):
        self.iid = iid
        self.datacenterdelay = -1
        self.servers = []
        self.requests = []

# ----------------------------
# READING DATA
# ----------------------------


V, E, R, C, X = map(int, input().split())

endpoitslst = [Endpoint(_) for _ in range(E)]
serverlst = [Server(_) for _ in range(C)]
videoslst = [Video(_) for _ in range(V)]

tmp = list(map(int, input().split()))

for i in range(V):
    videoslst[i].capacity = tmp[i]
for i in range(C):
    serverlst[i].capacity = X

print("Reading Endpoints")
for e in range(E):
    l, k = map(int, input().split())
    endpoitslst[e].datacenterdelay = l
    for i in range(k):
        c, l = map(int, input().split())
        endpoitslst[e].servers.append((c, l))
        serverlst[c].endpoints.append((e, l))

totalrequestnum = 0

requestslst = []  # (endpointiid, videoiid, quantity)

print("Reading Requests")
for r in range(R):
    v, e, n = map(int, input().split())
    endpoitslst[e].requests.append((v, n))
    totalrequestnum += n
    requestslst.append((e, v, n))

# ----------------------
# FUNCTIONS
# ----------------------


def find_server(serveriid):
    return serverlst[serveriid]


def request_criteria(r):
    endpointiid, videoiid, quantity = r
    video = videoslst[videoiid]
    endpoint = endpoitslst[endpointiid]
    return (quantity * endpoint.datacenterdelay ** 10) / (video.capacity ** (golden / 24))


def take_video_smart(endpointiid, videoiid, quantity):
    endpoint = endpoitslst[endpointiid]
    video = videoslst[videoiid]
    firstalready = -1
    firstfree = -1
    for i, item in enumerate(endpoint.servers):
        serveriid, delay = item
        server = find_server(serveriid)
        if(firstalready != -1 and firstfree != -1):
            break
        if(firstalready == -1):
            if(videoiid in server.videos):
                firstalready = i
        if(firstfree == -1):
            if(server.capacity >= video.capacity):
                firstfree = i
    if(firstalready == -1 and firstfree == -1):
        return
    if(firstalready == -1):
        server = find_server(firstfree)
        server.capacity -= video.capacity
        server.videos.append(video.iid)
        return
    # free, suitable
    delayfree = endpoint.servers[firstfree][1]
    delaysuitable = endpoint.servers[firstalready][1]
    delta = delaysuitable - delayfree
    global maxloss
    if(delta * quantity < maxloss):
        maxloss -= delta * quantity
        return
    server = find_server(firstfree)
    server.capacity -= video.capacity
    server.videos.append(video.iid)
    return


def take_video(endpointiid, videoiid):
    endpoint = endpoitslst[endpointiid]
    video = videoslst[videoiid]
    for item in endpoint.servers:
        server = find_server(item[0])
        if(video.iid in server.videos):
            return
        if(server.capacity < video.capacity):
            continue
        server.capacity -= video.capacity
        server.videos.append(video.iid)
        return


def get_score():
    print("Calculating result")
    saved = 0
    counter = 0
    for endpoint in endpoitslst:
        counter += 1
        percent = counter * 100 / E
        print("Processing : " + str(percent) + "%")
        for item in endpoint.requests:
            videoid = item[0]
            quantity = item[1]
            currentmin = endpoint.datacenterdelay * quantity
            for i in endpoint.servers:
                serveriid = i[0]
                delay = i[1]
                server = find_server(serveriid)
                if(videoid not in server.videos):
                    continue
                currentmin = min(currentmin, quantity * delay)
            saved += endpoint.datacenterdelay * quantity - currentmin
    result = saved * 1000 / totalrequestnum
    return result


def output():
    serverlst.sort(key=lambda n: n.iid)
    print(len(serverlst))
    for item in serverlst:
        print(item.iid, end=' ')
        for v in item.videos:
            print   (   v, end=' ')
        print()

# -----------------------
# SORTING REQUESTS
# -----------------------


print("Sorting")
requestslst.sort(key=lambda n: request_criteria(n), reverse=True)
for endpoint in endpoitslst:
    endpoint.servers.sort(key=lambda n: n[1])

# -----------------------
# TAKING VIDEOS
# -----------------------

print("Taking")
counter = 0
for item in requestslst:
    counter += 1
    if(counter % 1000 == 0):
        percent = (counter * 100) / (len(requestslst) * 2)
        print("Calculating: " + str(percent) + "%")
    endpointiid, videoiid, quantity = item
    take_video_smart(endpointiid, videoiid, quantity)

for item in requestslst:
    counter += 1
    if(counter % 1000 == 0):
        percent = (counter * 100) / (len(requestslst) * 2)
        print("Calculating: " + str(percent) + "%")
    endpointiid, videoiid, quantity = item
    take_video(endpointiid, videoiid)

print(get_score())
