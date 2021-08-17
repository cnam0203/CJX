import pandas as pd
import numpy as np
import jwt

from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.objects.conversion.dfg import converter as dfg_mining

from pm4py.visualization.petrinet import visualizer as pn_visualizer
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.visualization.dfg import visualizer as dfg_visualization

from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.conversion.process_tree import converter as pt_converter
from pm4py.objects.log.util import dataframe_utils

from pm4py.algo.evaluation.replay_fitness import algorithm as replay_fitness_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator


def get_process_discovery(touchpoints, type):
    # Format list touchpoints 
    df          = pd.DataFrame(touchpoints)
    gviz = None
    # Rename field in touchpoint into valid field
    df.rename(columns={'customer_id': 'case:concept:name',
              'action_type__name': 'concept:name', 'time': 'time:timestamp'}, inplace=True)
    df          = df.sort_values(by=['case:concept:name', 'time:timestamp'])
    log         = log_converter.apply(df)
    # Get process discovery graph bases on algorithm
    if type == "alpha":
        gviz = alpha_miner_algo(log)
    elif type == "heuristic-heu-net":
        gviz = heuristic_miner_heu_net(log)
    elif type == "heuristic-pet-net":
        gviz = heuristic_miner_petri_net(log)
    elif type == "dfg-discovery-frequency":
        gviz = dfg_discovery_frequency(log)
    elif type == "dfg-discovery-active-time":
        gviz = dfg_discovery_active_time(log)
    elif type == "dfg-discovery-pet-net":
        gviz = dfg_miner_petri(log)
    elif type == "inductive-miner-tree":
        gviz = inductive_miner_tree(log)
    elif type == "inductive-miner-petri":
        gviz = inductive_miner_petri_net(log)
    return gviz

def find_fitness(type, log, net, im, fm):
    fitness1 = replay_fitness_evaluator.apply(log, net, im, fm, variant=replay_fitness_evaluator.Variants.TOKEN_BASED)
    simp = simplicity_evaluator.apply(net)
    file = open("/Users/lap14458/Downloads/csv/evaluate.csv", "a")
    file.write(str(len(log)) + "," + type + "," + str(fitness1['perc_fit_traces']) + ',' + str(simp) + '\n')
    file.close()


def alpha_miner_algo(log):
    # alpha miner
    net, initial_marking, final_marking = alpha_miner.apply(log)
    find_fitness('alpha', log, net, initial_marking, final_marking)
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    return gviz, None


def heuristic_miner_heu_net(log):
    heu_net = heuristics_miner.apply_heu(log)
    gviz = hn_visualizer.apply(heu_net)
    return gviz, heu_net


def heuristic_miner_petri_net(log):
    # heuristic miner
    net, initial_marking, final_marking = heuristics_miner.apply(log)
    find_fitness('heu', log, net, initial_marking, final_marking)
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    return gviz, None


def dfg_discovery_active_time(log):
    # creatig the graph from log
    dfg = dfg_discovery.apply(log, variant=dfg_discovery.Variants.PERFORMANCE)
    gviz = dfg_visualization.apply(
        dfg, log=log, variant=dfg_visualization.Variants.PERFORMANCE)
    return gviz, None


def dfg_discovery_frequency(log):
    # creatig the graph from log
    dfg = dfg_discovery.apply(log)
    gviz = dfg_visualization.apply(
        dfg, log=log, variant=dfg_visualization.Variants.FREQUENCY)
    return gviz, None

def dfg_miner_petri(log):
    dfg = dfg_discovery.apply(log, variant=dfg_discovery.Variants.PERFORMANCE)
    net, im, fm = dfg_mining.apply(dfg)
    find_fitness('dfg', log, net, im, fm)
    gviz = pn_visualizer.apply(net, im, fm) 
    return gviz, None

def inductive_miner_tree(log):
    # create the process tree
    tree = inductive_miner.apply_tree(log)
    gviz = pt_visualizer.apply(tree)
    return gviz, None


def inductive_miner_petri_net(log):
    # create the process tree
    tree = inductive_miner.apply_tree(log)
    # convert the process tree to a petri net
    net, initial_marking, final_marking = pt_converter.apply(tree)
    find_fitness('induct', log, net, initial_marking, final_marking)
    parameters = {
        pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
    gviz = pn_visualizer.apply(net, initial_marking, final_marking,
                               parameters=parameters,
                               variant=pn_visualizer.Variants.FREQUENCY,
                               log=log)
    return gviz, None