from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.http import HttpResponse

from .models import Journey_Process_Graph
from .models import Clustered_Journey_Graph
from .models import Clustered_Customer
from .models import Journey_Cluster_Model
from journey.models import Touchpoint

from datetime import datetime
from sklearn.cluster import KMeans
from sklearn import preprocessing as sk_preprocessing
from kmodes.kmodes import KModes

import json
import pandas as pd
import numpy as np
import joblib

from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.process_tree import converter as pt_converter

from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery

from pm4py.visualization.petrinet import visualizer as pn_visualizer
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.visualization.dfg import visualizer as dfg_visualization

# Create your views here.
@user_passes_test(lambda user: user.is_staff, login_url='/admin')
def getClusterJourneyPage(request):
    return render(request, "graph_model/cluster-journey.html")


@user_passes_test(lambda user: user.is_staff, login_url='/admin')
def getVisualizeGraphPage(request):
    return render(request, "graph_model/visualize-graph.html", {"imgSrc": ''})

@user_passes_test(lambda user: user.is_staff, login_url='/admin')
def getClusterUserPage(request, id):
    return render(request, "graph_model/cluster-user.html", {"clusterID": id, "clusterSuccess": False})

@user_passes_test(lambda user: user.is_staff, login_url='/admin')
def getProcessGraph(request):
    if (request.method == "POST"):
        startDate, endDate = getPeriod(request)
        touchpoints = getListTouchpoints(startDate, endDate)

        if (len(touchpoints) == 0):
            return render(request, "graph_model/visualize-graph.html", {"result": "No available touchpoints"})

        type = request.POST["algorithm"]

        print(touchpoints)

        graph = processMining(touchpoints, type)
        graphLink = saveProcessGraph(graph, startDate, endDate, type)
        return render(request, "graph_model/visualize-graph.html", {"imgSrc": graphLink})

@user_passes_test(lambda user: user.is_staff, login_url='/admin')
def getClusterJourney(request):
    if (request.method == "POST"):
        startDate, endDate = getPeriod(request)
        touchpoints = getListTouchpoints(startDate, endDate)
        if (len(touchpoints) == 0):
            return render(request, "graph_model/cluster-journey.html", {"result": "No available touchpoints"})

        numClusters = int(request.POST["numClusters"])
        algorithm = request.POST["algorithmMethod"]
        preprocess = request.POST["preprocessMethod"]
        miningType = request.POST["miningAlgorithm"]
        user_journeys, customer_ids = create_journey(touchpoints)
        list_action_types = get_list_action_types(touchpoints)
        x_data = preprocessTouchpoint(
            user_journeys, list_action_types, preprocess)

        model = cluster_touchpoints(x_data, algorithm, numClusters)
        newClusterID, path = saveClusterModel(
            startDate=startDate, endDate=endDate, algorithm=algorithm, preprocess=preprocess, numClusters=numClusters, clusterModel=model)

        clusters, predict_journeys = predictJourneyCluster(algorithm, x_data, path)

        list_clustered_touchpoints = [[] for i in range(0, len(clusters))]

        for index, customer_id in enumerate(customer_ids):
            cluster_index = predict_journeys[index]
            user_touchpoints = [
                touchpoint for touchpoint in touchpoints if touchpoint["customer_id"] == customer_id]
            list_clustered_touchpoints[cluster_index] = list_clustered_touchpoints[cluster_index] + user_touchpoints
            print(cluster_index, ":", [touchpoint["action_type__name"]
                  for touchpoint in user_touchpoints])
            print("\n")

        graphLinks = []
        for index, clustered_touchpoint in enumerate(list_clustered_touchpoints):
            graph = processMining(clustered_touchpoint, miningType)
            graphLink = saveClusterGraph(
                graph, newClusterID, index, miningType)
            graphLinks.append(graphLink)

        return render(request, "graph_model/cluster-journey.html", {"graphLinks": graphLinks})

@user_passes_test(lambda user: user.is_staff, login_url='/admin')
def getClusterUser(request, id):
    if (request.method == "POST"):
        clusterID = id
        startDate, endDate = getPeriod(request)
        touchpoints = getListTouchpoints(startDate, endDate)

        if (len(touchpoints) == 0):
            return render(request, "graph_model/cluster-user.html", {"clusterID": clusterID, "result": "No available touchpoints"})

        clusterInfo = getClusterInfo(id)
        clusterGraphs = getClusterGraphs(id)

        algorithm = clusterInfo[0]["algorithm"]
        preprocess = clusterInfo[0]["preprocessing"]
        clusterModelFile = clusterInfo[0]["clusterModelFile"]

        user_journeys, customer_ids = create_journey(touchpoints)
        list_action_types = get_list_action_types(touchpoints)
        x_data = preprocessTouchpoint(
            user_journeys, list_action_types, preprocess)

        clusters, predict_journeys = predictJourneyCluster(algorithm, x_data, clusterModelFile)

        list_clustered_touchpoints = [[] for i in range(0, len(clusters))]

        for index, customer_id in enumerate(customer_ids):
            cluster_index = predict_journeys[index]
            user_touchpoints = [touchpoint["action_type__name"]
                                for touchpoint in touchpoints if touchpoint["customer_id"] == customer_id]

            graph_index = [index for index, clusterGraph in enumerate(
                clusterGraphs) if clusterGraph["clusterNumber"] == cluster_index][0]

            cluster_number_id = clusterGraphs[graph_index]["id"]

            saveClusteredUser(customer_id, startDate, endDate,
                              user_touchpoints, cluster_number_id)

        return render(request, "graph_model/cluster-user.html", {"clusterID": clusterID, "clusterSuccess": True})

def getPeriod(request):
    startDate = datetime(2000, 1, 1)
    endDate = datetime.now()
    if (request.POST["startDate"] != ''):
        startDate = request.POST["startDate"]
    if (request.POST["endDate"] != ''):
        endDate = request.POST["endDate"]

    return startDate, endDate

def getListTouchpoints(startDate, endDate):
    touchpoints = Touchpoint.objects.filter(visit_time__range=[startDate, endDate]).values(
        'customer_id', 'visit_time', 'action_type__name')
    touchpoints = list(touchpoints)

    return touchpoints

def getClusterInfo(clusterId):
    clusterInfo = Journey_Cluster_Model.objects.filter(id=clusterId).values(
        'id', 'algorithm', 'preprocessing', 'preprocessingModelFile', 'clusterModelFile')
    return list(clusterInfo)

def getClusterGraphs(clusterId):
    clusterGraphs = Clustered_Journey_Graph.objects.filter(clusterID=clusterId).values(
        'id', 'clusterNumber', 'clusterName', 'link')
    return list(clusterGraphs)

def load_model(path):
    return joblib.load(path)

def get_list_action_types(touchpoints):
    df = pd.DataFrame(touchpoints)
    list_action_types = df["action_type__name"].unique()
    return list_action_types

def create_journey(touchpoints):
    df = pd.DataFrame(touchpoints)
    list_journeys = []
    list_userID = df["customer_id"].unique()
    for userID in list_userID:
        user_journey = df.loc[df["customer_id"] ==
                              userID, ["action_type__name", "visit_time"]]
        user_journey = user_journey.sort_values(
            ['visit_time'], ascending=[True])
        user_journey = user_journey["action_type__name"].tolist()
        list_journeys.append(user_journey)

    return list_journeys, list_userID

def cluster_touchpoints(x_data, algorithm, numClusters):
    if (algorithm == "kmeans"):
        model = kmeans_clustering(x_data, numClusters)
    elif (algorithm == "kmodes"):
        model = kmodes_clustering(x_data, numClusters)
    return model

def kmeans_clustering(x_data, numClusters):
    kmeans = KMeans(n_clusters=numClusters, random_state=0).fit(x_data)
    return kmeans

def kmodes_clustering(x_data, numClusters):
    kmodes = KModes(n_clusters=numClusters).fit(x_data)
    return kmodes

def preprocessTouchpoint(user_journeys, list_action_types, preprocess):
    preprocessed_touchpoints = np.array([])
    if (preprocess == "bagOfActivities"):
        preprocessed_touchpoints = preprocess_bag_of_activities(
            user_journeys, list_action_types)
    if (preprocess == "sequenceVector"):
        preprocessed_touchpoints = preprocess_sequence_vector(
            user_journeys, list_action_types)
    return preprocessed_touchpoints

def preprocess_bag_of_activities(user_journeys, list_action_types):
    list_touchpoint_vectors = []
    for journey in user_journeys:
        touchpoint_vector = []
        for action_type in list_action_types:
            touchpoint_vector.append(journey.count(action_type))
        list_touchpoint_vectors.append(touchpoint_vector)

    return list_touchpoint_vectors


def preprocess_sequence_vector(user_journeys, list_action_types):
    list_touchpoint_vectors = []
    label = sk_preprocessing.LabelEncoder()
    label.fit(list_action_types)

    for journey in user_journeys:
        label_transform = []
        for value in label.transform(journey).tolist():
            label_transform.append(value+1)
        list_touchpoint_vectors.append(label_transform)

    max_len = max([len(x) for x in list_touchpoint_vectors])
    x_data = [np.pad(x, (0, max_len - len(x)), 'constant').tolist()
              for x in list_touchpoint_vectors]
    return x_data


def processMining(touchpoints, type):
    df = pd.DataFrame(touchpoints)
    df["visit_time"] = pd.to_datetime(df['visit_time'], unit='s')
    df = dataframe_utils.convert_timestamp_columns_in_df(df)
    df.rename(columns={'customer_id': 'case:concept:name',
              'action_type__name': 'concept:name', 'visit_time': 'time:timestamp'}, inplace=True)
    df = df.sort_values(by=['case:concept:name', 'time:timestamp'])
    log = log_converter.apply(df)

    gviz = None

    if type == "alpha":
        gviz = alphaMiner(log)
    elif type == "heuristic-heu-net":
        gviz = heuristicMinerHeuNet(log)
    elif type == "heuristic-pet-net":
        gviz = heuristicMinerPetriNet(log)
    elif type == "dfg-discovery-frequency":
        gviz = dfgDiscoveryFrequency(log)
    elif type == "dfg-discovery-active-time":
        gviz = dfgDiscoveryActiveTime(log)
    elif type == "inductive-miner-tree":
        gviz = InductiveMinerTree(log)
    elif type == "inductive-miner-petri":
        gviz = InductiveMinerPetriNet(log)

    return gviz


def alphaMiner(log):
    # alpha miner
    net, initial_marking, final_marking = alpha_miner.apply(log)
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    return gviz

def heuristicMinerHeuNet(log):
    heu_net = heuristics_miner.apply_heu(log)
    gviz = hn_visualizer.apply(heu_net)
    return gviz


def heuristicMinerPetriNet(log):
    # heuristic miner
    net, initial_marking, final_marking = heuristics_miner.apply(log)
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    return gviz


def dfgDiscoveryActiveTime(log):
    # creatig the graph from log
    dfg = dfg_discovery.apply(log, variant=dfg_discovery.Variants.PERFORMANCE)
    gviz = dfg_visualization.apply(
        dfg, log=log, variant=dfg_visualization.Variants.PERFORMANCE)
    return gviz


def dfgDiscoveryFrequency(log):
    # creatig the graph from log
    dfg = dfg_discovery.apply(log)
    gviz = dfg_visualization.apply(
        dfg, log=log, variant=dfg_visualization.Variants.FREQUENCY)
    return gviz


def InductiveMinerTree(log):
    # create the process tree
    tree = inductive_miner.apply_tree(log)
    gviz = pt_visualizer.apply(tree)
    return gviz


def InductiveMinerPetriNet(log):
    # create the process tree
    tree = inductive_miner.apply_tree(log)
    # convert the process tree to a petri net
    net, initial_marking, final_marking = pt_converter.apply(tree)
    parameters = {
        pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
    gviz = pn_visualizer.apply(net, initial_marking, final_marking,
                               parameters=parameters,
                               variant=pn_visualizer.Variants.FREQUENCY,
                               log=log)
    return gviz

def predictJourneyCluster(algorithm, x_data, clusterModelFile):
        loaded_model = load_model(clusterModelFile)

        if (algorithm == "kmeans"):
            clusters = loaded_model.cluster_centers_
        elif (algorithm == "kmodes"):
            clusters = loaded_model.cluster_centroids_

        predict_journeys = loaded_model.predict(x_data)

        return clusters, predict_journeys


def saveProcessGraph(gviz, startDate, endDate, type):
    filename = '/graph_model/journeyProcessGraph/' + str(datetime.now().timestamp()) + ".png"
    path = "graph_model/static" + filename
    staticPath = '/static' + filename
    saveGraphFile(type, gviz, path)
    newGraph = Journey_Process_Graph.objects.create(runDate=datetime.now(
    ), startDate=startDate, endDate=endDate, type=type, link=staticPath)
    newGraph.save()

    return filename


def saveClusterGraph(gviz, clusterID, clusterNumber, type, clusterName=None):
    filename = '/graph_model/journeyClusterGraph/' + str(datetime.now().timestamp()) + ".png"
    path = "graph_model/static" + filename
    staticPath = '/static' + filename
    saveGraphFile(type, gviz, path)
    newGraph = Clustered_Journey_Graph.objects.create(
        clusterID=clusterID, clusterNumber=clusterNumber, clusterName=clusterName, type=type, link=staticPath)
    newGraph.save()

    return filename

def saveGraphFile(type, gviz, path):
    if type == "alpha":
        pn_visualizer.save(gviz, path)
    elif type == "heuristic-heu-net":
        hn_visualizer.save(gviz, path)
    elif type == "heuristic-pet-net":
        pn_visualizer.save(gviz, path)
    elif type == "dfg-discovery-frequency":
        dfg_visualization.save(gviz, path)
    elif type == "dfg-discovery-active-time":
        dfg_visualization.save(gviz, path)
    elif type == "inductive-miner-tree":
        pt_visualizer.save(gviz, path)
    elif type == "inductive-miner-petri":
        pn_visualizer.save(gviz, path)
        

def saveClusterModel(startDate, endDate, algorithm, preprocess, numClusters,  clusterModel, preprocessModel=None, accuracy=0):
    filename = '/graph_model/journeyClusterModel/' + str(datetime.now().timestamp()) + ".sav"
    path = "graph_model/static" + filename
    joblib.dump(clusterModel, path)

    newModel = Journey_Cluster_Model.objects.create(startDate=startDate,
                                      endDate=endDate,
                                      algorithm=algorithm,
                                      preprocessing=preprocess,
                                      numberClusters=numClusters,
                                      clusterModelFile=path, preprocessingModelFile='', accuracy=accuracy)

    newModel.save()
    return newModel.id, path

def saveClusteredUser(userID, startJourneyDate, endJourneyDate, journey, cluster_number_id):
    cluster = Clustered_Journey_Graph.objects.get(id=cluster_number_id)
    newClusteredUser = Clustered_Customer.objects.create(customer_id=userID,
                                                    fromDate=startJourneyDate,
                                                    toDate=endJourneyDate,
                                                    journey=journey,
                                                    cluster=cluster)
    newClusteredUser.save()



