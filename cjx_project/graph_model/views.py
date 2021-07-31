from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.apps import apps
from django.contrib.auth.decorators import login_required

from .models import Journey_Process_Graph, Clustered_Journey_Graph, Clustered_Customer, Journey_Cluster_Model, Decision_Process_Graph, Decision_Action_Graph
from .decision_mining import build_tree, print_tree
from .process_mining import get_process_discovery
from .clustering import kmeans_clustering, kmodes_clustering
from .constant import formData, mining_algorithms, preprocessing_methods, clustering_algorithms

from pm4py.visualization.petrinet import visualizer as pn_visualizer
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.visualization.dfg import visualizer as dfg_visualization
from sklearn import preprocessing as sk_preprocessing

import operator
import math
import json
import pandas as pd
import numpy as np
import joblib

from datetime import datetime
from graphviz import Digraph
from journey.models import Touchpoint
from utils.copy_object import copy_object
from utils.path_helper import get_static_path
# Create your views here.


@login_required(login_url="/authentication/login")
def visualize_process_graph(request):
    return render(
                    request, 
                    "graph_model/visualize-process-graph.html", 
                    {
                        "mining_algorithms": mining_algorithms
                    }
                )


@login_required(login_url="/authentication/login")
def trace_clustering(request):
    return render(
                    request, 
                    "graph_model/trace-clustering.html", 
                    {
                        "preprocessing_methods" : preprocessing_methods,
                        "clustering_algorithms" : clustering_algorithms,
                        "mining_algorithms"     : mining_algorithms
                    }
                )


@login_required(login_url="/authentication/login")
def decision_mining(request):
    return render(
                    request, 
                    "graph_model/decision-mining.html"
                )


@login_required(login_url="/authentication/login")
def get_list_data(request, tablename):
    Model       = apps.get_model(app_label="graph_model", model_name=tablename)
    data        = list(Model.objects.all().values())
    headers     = []
    new_data    = []

    if (tablename == "journey_process_graph"):
        headers = ['id', 'startDate', 'endDate', 'runDate', 'miningAlgorithm', 'processGraph']

        for obj in data:
            obj['miningAlgorithm']          = obj["type"]
            obj['processGraph']             = {}
            obj['processGraph']['link']     = obj["link"]
            obj['processGraph']['value']    = 'view'

            new_obj = copy_object(obj, headers)
            new_data.append(new_obj)
        
    elif (tablename == "clustered_journey_graph"):
        headers = ['id', 'clusterModel', 'clusterNumber', 'clusterName', 'miningAlgorithm', 'processGraph']

        for obj in data:
            obj['miningAlgorithm']          = obj["type"]
            obj['processGraph']             = {}
            obj['processGraph']['link']     = obj["link"]
            obj['processGraph']['value']    = 'view'
        
            obj['clusterModel']             = {}
            obj['clusterModel']['link']     = "/graph_model/form/update/journey_cluster_model/" + str(obj["clusterModelID"])
            obj['clusterModel']['value']    = str(obj["clusterModelID"])

            new_obj = copy_object(obj, headers)
            new_data.append(new_obj)

    elif (tablename == "journey_cluster_model"):
        headers = ("id", "runDate", "algorithm", "preprocessing", "numberClusters", "accuracy", "clusterCustomer")

        for obj in data:
            obj["clusterCustomer"]          = {}
            obj["clusterCustomer"]['link']  = "/graph_model/analytics/cluster-customer/" + str(obj["id"])
            obj["clusterCustomer"]['value'] = 'Cluster now'

            new_obj = copy_object(obj, headers)
            new_data.append(new_obj)

    elif (tablename == "clustered_customer"):
        headers = ["id", "customer_id", "clusterID", "clusterGroup", "fromDate", "toDate", "journey", "clusterProcessGraph"]

        for obj in data:
            cluster_id  = obj["cluster_id"]
            cluster     = Clustered_Journey_Graph.objects.get(pk=cluster_id)

            obj["clusterGroup"]         = cluster.clusterName
            obj["clusterID"]            = {}
            obj["clusterID"]['link']    = "/graph_model/form/update/clustered_journey_graph/" + str(cluster_id)
            obj["clusterID"]['value']   = str(cluster_id)

            obj["clusterProcessGraph"]          = {}
            obj["clusterProcessGraph"]['link']  = cluster.link
            obj["clusterProcessGraph"]['value'] = 'view'

            new_obj = copy_object(obj, headers)
            new_data.append(new_obj)

    elif (tablename == "decision_process_graph"):
        headers = ["id", "startDate", "endDate", "runDate", "journeyProcess", "processGraph", "decisionGraph"]

        for obj in data:
            obj["journeyProcess"]           = {}
            obj["journeyProcess"]['link']   = "/graph_model/form/update/journey_process_graph/" + str(obj["journeyProcessID"])
            obj["journeyProcess"]['value']  = obj["journeyProcessID"]

            obj["processGraph"]             = {}
            obj["processGraph"]['link']     = obj["processGraphLink"]
            obj["processGraph"]['value']    = 'view'

            obj["decisionGraph"]            = {}
            obj["decisionGraph"]['link']    = obj["decisionGraphLink"]
            obj["decisionGraph"]['value']   = 'view'

            new_obj = copy_object(obj, headers)
            new_data.append(new_obj)

    elif (tablename == "decision_action_graph"):
        headers = ["id", "action", "decisionProcess", "actionGraph"]

        for obj in data:
            obj["decisionProcess"]          = {}
            obj["decisionProcess"]['link']  = "/graph_model/form/update/decision_process_graph/" + str(obj["decisionProcessID"])
            obj["decisionProcess"]['value'] = obj["decisionProcessID"]

            obj["actionGraph"]              = {}
            obj["actionGraph"]['link']      = obj["actionGraphLink"]
            obj["actionGraph"]['value']     = 'view'

            new_obj = copy_object(obj, headers)
            new_data.append(new_obj)

    return render(
                    request, 
                    "graph_model/base-table.html", 
                    {
                        'data': new_data, 
                        'tableName': tablename, 
                        'headers': headers
                    }
                )


@login_required(login_url="/authentication/login")
def update_form_data(request, tablename, id=None):
    Model = apps.get_model(app_label="graph_model", model_name=tablename)
    FormModel = formData[tablename]
    obj = get_object_or_404(Model, pk=id)
    form = FormModel(instance=obj)

    if request.method == "POST":
        form = FormModel(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/graph_model/table/" + tablename) 
    
    return render(
                    request, 
                    "graph_model/base-form.html", 
                    {
                        'formName': 'Form ' + tablename, 
                        'form': form
                    }
                )


@login_required(login_url="/authentication/login")
def cluster_customer(request, id):
    return render(
                    request, 
                    "graph_model/cluster-customer.html", 
                    {
                        "clusterID": id, 
                        "clusterSuccess": False
                    }
                )


@login_required(login_url="/authentication/login")
def get_cluster_journey_page(request):
    return render(
                    request, 
                    "graph_model/cluster-journey.html"
                )


@login_required(login_url="/authentication/login")
def get_visualize_graph_page(request):
    return render(
                    request, 
                    "graph_model/visualize-graph.html", 
                    {
                        "imgSrc": ''
                    }
                )


@login_required(login_url="/authentication/login")
def get_cluster_user_page(request, id):
    return render(
                    request, 
                    "graph_model/cluster-user.html", 
                    {
                        "clusterID"     : id, 
                        "clusterSuccess": False
                    })


@login_required(login_url="/authentication/login")
def get_customer_process_discovery(request):
    if (request.method == "POST"):
        startDate, endDate  = get_period(request)
        touchpoints         = get_list_touchpoints(startDate, endDate)

        # Check whether data exists in time range
        if (len(touchpoints) == 0):
            return render(
                            request, 
                            "graph_model/visualize-process-graph.html", 
                            {
                                "result": "No available touchpoints"
                            }
                        )

        # Get customer process discovry
        mining_algorithm    = request.POST["mining-algorithm"]
        graph, net          = get_process_discovery(touchpoints, mining_algorithm)
        graphLink, processGraphID, processGraphLink = save_process_graph(graph, startDate, endDate, mining_algorithm)

        return render(
                        request, 
                        "graph_model/visualize-process-graph.html", 
                        {
                            "imgSrc"            : graphLink, 
                            "mining_algorithms" : mining_algorithms
                        }
                    )


@login_required(login_url="/authentication/login")
def get_decision_graph(request):
    if (request.method == "POST"):
        startDate, endDate  = get_period(request)
        touchpoints         = get_list_touchpoints(startDate, endDate)
        touchpoints.sort(key=lambda touchpoint: touchpoint['time'])

        # Check whether data exists in time range
        if (len(touchpoints) == 0):
            return render(
                            request, 
                            "graph_model/decision-mining.html", 
                            {
                                "result": "No available touchpoints"
                            }
                        )
        
        # Get customer process discovery by using heuristic mining
        mining_algorithm    = "heuristic-heu-net"
        graph, net          = get_process_discovery(touchpoints, mining_algorithm)
        processGraph, processGraphID, processGraphLink = save_process_graph(graph, startDate, endDate, mining_algorithm)

        # Convert a heuristic net into a array
        net_arr             = convert_net_to_arr(net)

        # Prepare data for decision tree
        list_attributes     = ['device_category__name', 'device_os__name', 'device_browser__name', 'action_type__name']
        X_data              = get_decison_tree_input_data(touchpoints, net_arr, list_attributes)

        big_tree_view = Digraph(format='png')
        list_trees = []

        # Find decision tree for each action
        for action_name in X_data:
            action_touchpoints = X_data[action_name]

            if len(action_touchpoints) > 0:
                decision_tree = build_tree(action_touchpoints)
                curr_tree_view = Digraph(format='png')

                curr_tree_view.node(action_name, label=str(action_name), shape='oval', color='red')
                big_tree_view.node(action_name, label=str(action_name), shape='oval', color='red')

                print_tree(decision_tree, big_tree_view, list_attributes, True, action_name)
                print_tree(decision_tree, curr_tree_view, list_attributes, True, action_name)

                list_trees.append({'tree_view': curr_tree_view, 'name': action_name})

        # Save graph into database
        graphLinks = []
        decisionGraph, decisionProcessID = save_decision_graph(big_tree_view, startDate, endDate, processGraphID, processGraphLink)

        for tree in list_trees:
            graphLink = save_action_graph(tree['tree_view'], tree['name'], decisionProcessID)
            graphLinks.append(graphLink)

        return render(
                        request, 
                        "graph_model/decision-mining.html", 
                        {
                            "processGraph": processGraph, 
                            "decisionGraph": decisionGraph, 
                            "graphLinks": graphLinks
                        }
                    )

@login_required(login_url="/authentication/login")
def get_trace_clustering(request):
    if (request.method == "POST"):
        startDate, endDate  = get_period(request)
        touchpoints         = get_list_touchpoints(startDate, endDate)

        # Check whether data exists in time range
        if (len(touchpoints) == 0):
            return render(
                            request, 
                            "graph_model/trace-clustering.html", 
                            {
                                "result": "No available touchpoints",
                                "preprocessing_methods": preprocessing_methods,
                                "clustering_algorithms": clustering_algorithms,
                                "mining_algorithms": mining_algorithms
                            }
                        )

        # Get config info
        numClusters         = int(request.POST["numClusters"])
        algorithm           = request.POST["algorithmMethod"]
        preprocessMethod    = request.POST["preprocessMethod"]
        miningAlgorithm     = request.POST["miningAlgorithm"]

        # Preprocess data
        user_journeys, customer_ids = create_journey(touchpoints)
        list_action_types           = get_unique_values(touchpoints, 'action_type__name')
        X_data                      = preprocess_journey(user_journeys, list_action_types, preprocessMethod)
        # Run clustering algorithm and save model
        model = cluster_journeys(X_data, algorithm, numClusters)
        newClusterID, model_path = save_cluster_model(
                            startDate=startDate, endDate=endDate, algorithm=algorithm, 
                            preprocess=preprocessMethod, numClusters=numClusters, clusterModel=model)

        # Find predict cluster for each journey
        clusters, Y_predict = predict_journey_cluster(algorithm, X_data, model_path)

        list_clustered_journeys = [[] for i in range(0, len(clusters))]

        for index, customer_id in enumerate(customer_ids):
            # Get cluster index 
            cluster_index = Y_predict[index]
            # Get journey of each customer
            user_journey = [touchpoint for touchpoint in touchpoints if touchpoint["customer_id"] == customer_id]
            # Append journey in accurate cluster
            list_clustered_journeys[cluster_index] = list_clustered_journeys[cluster_index] + user_journey

        # Save database
        graphLinks = []
        for index, clustered_journey in enumerate(list_clustered_journeys):
            graph, net = get_process_discovery(clustered_journey, miningAlgorithm)
            graphLink = save_cluster_graph(
                graph, newClusterID, index, miningAlgorithm)
            graphLinks.append(graphLink)

        return render(
                        request, 
                        "graph_model/trace-clustering.html", 
                        {
                            "graphLinks": graphLinks,
                            "preprocessing_methods": preprocessing_methods,
                            "clustering_algorithms": clustering_algorithms,
                            "mining_algorithms": mining_algorithms
                        }
                    )


@login_required(login_url="/authentication/login")
def get_cluster_user(request, id):
    if (request.method == "POST"):
        clusterID               = id
        startDate, endDate      = get_period(request)
        touchpoints             = get_list_touchpoints(startDate, endDate)

        if (len(touchpoints) == 0):
            return render(
                            request, 
                            "graph_model/cluster-customer.html", 
                            {
                                "clusterID": clusterID, 
                                "result": "No available touchpoints"
                            }
                        )

        # Get information about clustered model
        clusterInfo     = get_cluster_info(id)
        clusterGraphs   = get_cluster_graphs(id)


        # Get config information of clustered model
        algorithm = clusterInfo[0]["algorithm"]
        preprocess = clusterInfo[0]["preprocessing"]
        clusterModelFile = clusterInfo[0]["clusterModelFile"]

        # Preprocess data
        user_journeys, customer_ids = create_journey(touchpoints)
        list_action_types = get_unique_values(touchpoints, 'action_type__name')
        X_data = preprocess_journey(user_journeys, list_action_types, preprocess)

        # Predict cluster for customer journey
        clusters, Y_predict = predict_journey_cluster(algorithm, X_data, clusterModelFile)
        list_clustered_journeys = [[] for i in range(0, len(clusters))]

        # Assign customer into journey cluster
        for index, customer_id in enumerate(customer_ids):
            # Get predict cluster for customer journey
            cluster_index   = Y_predict[index]
            # Get user journey
            user_journey    = [touchpoint["action_type__name"] for touchpoint in touchpoints if touchpoint["customer_id"] == customer_id]
            graph_index = [index for index, clusterGraph in enumerate(
                clusterGraphs) if clusterGraph["clusterNumber"] == cluster_index][0]

            cluster_graph_id = clusterGraphs[graph_index]["id"]
            save_clustered_user(customer_id, startDate, endDate,
                              user_journey, cluster_graph_id)

        return render(
                        request, 
                        "graph_model/cluster-customer.html", 
                        {
                            "clusterID": clusterID, 
                            "clusterSuccess": True
                        }
                    )


def get_decison_tree_input_data(touchpoints, net_arr, list_attributes):
        journeys        = {}  # list journeys for each customer,        Ex: journeys = {'cust_1': ['login', 'buy'], 'cust_2': ['buy']}
        X_data          = {}  # list touchpoints following by an action Ex: actions  = {'login': [touchpoint_1, touchpoint_2], 'view_proudct': [touchpoint_3]} 
        unique_actions  = get_unique_values(touchpoints, 'action_type__name')
        unique_actions.insert(0, 'start')
        
        for touchpoint in touchpoints:
            customer_id = touchpoint['customer_id']
            if customer_id not in journeys:
                journeys[customer_id] = []
            journeys[customer_id].append(touchpoint) 

        for action in unique_actions:
            X_data[action] = []

        for customer_id in journeys:
            for idx, touchpoint in enumerate(journeys[customer_id]):
                if (idx == 0):
                    next_touchpoint = journeys[customer_id][idx]
                    cur_action_name = 'start'
                elif (idx < len(journeys[customer_id]) - 1):
                    next_touchpoint = journeys[customer_id][idx+1]
                    cur_action_name = touchpoint['action_type__name']
                else:
                    next

                if (next_touchpoint['action_type__name'] in net_arr[cur_action_name]):
                    x = []
                    for attribute in list_attributes:
                        x.append(next_touchpoint[attribute])
                    X_data[cur_action_name].append(x)

        return X_data


def convert_net_to_arr(net):
    net_arr             = {}
    net_arr['start']    = []

    for node_name in net.start_activities[0]:
        net_arr['start'].append(node_name)

    for node_name in net.nodes:
        node                = net.nodes[node_name]
        net_arr[node_name]  = []

        for idx, conn in enumerate(node.output_connections.keys()):
            net_arr[node_name].append(conn.node_name)

    return net_arr

def save_decision_graph(tree, startDate, endDate, journeyProcessID, processGraphLink):
    filename = 'graph_model/decisionGraph/' + str(datetime.now().timestamp()) + ".gv"
    (static_path, link_url) = get_static_path(filename, 'graph_model')
    
    tree.render(static_path)
    filename = filename + '.png'
    link_url = link_url + '.png'

    newGraph = Decision_Process_Graph.objects.create(
        runDate=datetime.now(), startDate=startDate, endDate=endDate, journeyProcessID=journeyProcessID,
        processGraphLink=processGraphLink, decisionGraphLink=link_url)
    newGraph.save()

    return filename, newGraph.id

def save_action_graph(tree, actionName, decisionMiningID):
    filename = 'graph_model/decisionGraph/' + str(datetime.now().timestamp()) + ".gv"
    (static_path, link_url) = get_static_path(filename, 'graph_model')
    
    tree.render(static_path)
    filename = filename + '.png'
    link_url = link_url + '.png'

    newGraph = Decision_Action_Graph.objects.create(action=actionName, decisionProcessID=decisionMiningID, actionGraphLink=link_url)
    newGraph.save()

    return filename


def get_period(request):
    startDate = datetime(2000, 1, 1)
    endDate = datetime.now()
    if (request.POST["startDate"] != ''):
        startDate = request.POST["startDate"]
    if (request.POST["endDate"] != ''):
        endDate = request.POST["endDate"]

    return startDate, endDate


def get_list_touchpoints(startDate, endDate):
    touchpoints = Touchpoint.objects.filter(time__range=[startDate, endDate]).values(
        'customer_id', 'time', 'action_type__name', 'device_browser__name', 'device_os__name', 'device_category__name')
    touchpoints = list(touchpoints)

    return touchpoints


def get_cluster_info(clusterId):
    clusterInfo = Journey_Cluster_Model.objects.filter(id=clusterId).values(
        'id', 'algorithm', 'preprocessing', 'preprocessingModelFile', 'clusterModelFile')
    return list(clusterInfo)


def get_cluster_graphs(clusterId):
    clusterGraphs = Clustered_Journey_Graph.objects.filter(clusterModelID=clusterId).values(
        'id', 'clusterNumber', 'clusterName', 'link')
    return list(clusterGraphs)


def load_model(path):
    return joblib.load(path)


def get_unique_values(touchpoints, column):
    df = pd.DataFrame(touchpoints)
    list_values = df[column].unique()
    return list(list_values)


def create_journey(touchpoints):
    df = pd.DataFrame(touchpoints)
    list_journeys = []
    list_userID = df["customer_id"].unique()

    for userID in list_userID:
        user_journey = df.loc[df["customer_id"] ==
                              userID, ["action_type__name", "time"]]
        user_journey = user_journey.sort_values(['time'], ascending=[True])
        user_journey = user_journey["action_type__name"].tolist()
        list_journeys.append(user_journey)

    return list_journeys, list_userID


def cluster_journeys(X_data, algorithm, numClusters):
    if (algorithm == "k-means"):
        model = kmeans_clustering(X_data, numClusters)
    elif (algorithm == "k-modes"):
        model = kmodes_clustering(X_data, numClusters)
    return model


def preprocess_journey(user_journeys, list_action_types, preprocessing_method):
    preprocessed_journeys = np.array([])
    if (preprocessing_method == "bag-of-activities"):
        preprocessed_journeys = preprocess_bag_of_activities(
            user_journeys, list_action_types)
    elif (preprocessing_method == "sequence-vector"):
        preprocessed_journeys = preprocess_sequence_vector(
            user_journeys, list_action_types)
    return preprocessed_journeys


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
    X_data = [np.pad(x, (0, max_len - len(x)), 'constant').tolist()
              for x in list_touchpoint_vectors]
    return X_data


def predict_journey_cluster(algorithm, X_data, clusterModelFile):
    loaded_model = load_model(clusterModelFile)

    if (algorithm == "k-means"):
        clusters = loaded_model.cluster_centers_
    elif (algorithm == "k-modes"):
        clusters = loaded_model.cluster_centroids_

    Y_predict = loaded_model.predict(X_data)

    return clusters, Y_predict


def save_process_graph(gviz, startDate, endDate, type):
    filename = 'graph_model/journeyProcessGraph/' + \
        str(datetime.now().timestamp()) + ".png"

    (static_path, link_url) = get_static_path(filename, 'graph_model')
    save_graph_file(type, gviz, static_path)

    newGraph = Journey_Process_Graph.objects.create(runDate=datetime.now(
    ), startDate=startDate, endDate=endDate, type=type, link=link_url)
    newGraph.save()

    return filename, newGraph.id, link_url


def save_cluster_graph(gviz, clusterID, clusterNumber, type, clusterName=None):
    filename = 'graph_model/journeyClusterGraph/' + \
        str(datetime.now().timestamp()) + ".png"

    (static_path, link_url) = get_static_path(filename, 'graph_model')
    save_graph_file(type, gviz, static_path)
    newGraph = Clustered_Journey_Graph.objects.create(clusterModelID=clusterID, clusterNumber=clusterNumber, clusterName=clusterName, type=type, link=link_url)
    newGraph.save()

    return filename


def save_graph_file(type, gviz, path):
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
    elif type == "dfg-discovery-pet-net":
        pt_visualizer.save(gviz, path)
    elif type == "inductive-miner-tree":
        pt_visualizer.save(gviz, path)
    elif type == "inductive-miner-petri":
        pn_visualizer.save(gviz, path)


def save_cluster_model(startDate, endDate, algorithm, preprocess, numClusters,  clusterModel, preprocessModel=None, accuracy=0):
    filename = 'graph_model/journeyClusterModel/' + str(datetime.now().timestamp()) + ".sav"
    (static_path, link_url) = get_static_path(filename, 'graph_model')
    joblib.dump(clusterModel, static_path)

    newModel = Journey_Cluster_Model.objects.create(startDate=startDate,
                                                    endDate=endDate,
                                                    algorithm=algorithm,
                                                    preprocessing=preprocess,
                                                    numberClusters=numClusters,
                                                    clusterModelFile=static_path, preprocessingModelFile='', accuracy=accuracy)

    newModel.save()
    return newModel.id, static_path


def save_clustered_user(userID, startJourneyDate, endJourneyDate, journey, cluster_number_id):
    cluster = Clustered_Journey_Graph.objects.get(id=cluster_number_id)
    newClusteredUser = Clustered_Customer.objects.create(customer_id=userID,
                                                         fromDate=startJourneyDate,
                                                         toDate=endJourneyDate,
                                                         journey=journey,
                                                         cluster=cluster)
    newClusteredUser.save()