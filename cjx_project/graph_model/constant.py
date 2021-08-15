from .forms import Journey_Process_Graph_Form, Clustered_Journey_Graph_Form, Clustered_Customer_Form, Journey_Cluster_Model_Form, Decision_Action_Graph_Form, Decision_Process_Graph_Form

formData = {
    'journey_cluster_model'     : Journey_Cluster_Model_Form,
    'clustered_journey_graph'   : Clustered_Journey_Graph_Form,
    'clustered_customer'        : Clustered_Customer_Form,
    'journey_process_graph'     : Journey_Process_Graph_Form,
    'decision_process_graph'    : Decision_Process_Graph_Form,
    'decision_action_graph'     : Decision_Action_Graph_Form,
}

mining_algorithms = [
        {
            "value" : "alpha", 
            "name"  : "Alpha Miner with Petri Net"
        },
        {
            "value" : "heuristic-heu-net", 
            "name"  : "Heuristic Miner with Heuristic Net"
        },
        {
            "value" : "heuristic-pet-net", 
            "name"  : "Heuristic Miner with Petri Net"
        },
        {   "value" : "inductive-miner-tree", 
            "name"  : "Inductive Miner with Tree Graph"
        },
        {   
            "value" : "inductive-miner-petri", 
            "name"  : "Inductive Miner with Petri Net"
        }
    ]

preprocessing_methods = [
        {
            "value" : "bag-of-activities", 
            "name"  : "Bag of Activities"
        },
        {   
            "value" : "sequence-vector", 
            "name"  : "Sequence vector"
        },
    ]

clustering_algorithms = [
        {
            "value" : "k-means", 
            "name"  : "K-Means"
        },
        {
            "value" : "k-modes", 
            "name"  : "K-Modes"
        },
    ]