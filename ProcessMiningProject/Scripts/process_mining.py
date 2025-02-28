import os

import pm4py  # version 2.7.4
from pprint import pprint  # pretty printing
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.evaluation import algorithm as evaluation
from pm4py.objects.conversion.log import converter as stream_converter
from pm4py.objects.log.importer.xes import importer as xes_import
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay

def load_event_log(file_path):
    log = xes_import.apply(file_path)
    log_df = pm4py.convert.convert_to_dataframe(log)  # Convert log to DataFrame
    log = pm4py.convert_to_event_log(log)  # Convert log to EventLog
    return log, log_df

def print_trace_and_event_structure(log):
    print("\n 2 ____________________________________________________________ \n")
    print("Trace keys:")
    print(list(log[0].attributes.keys()))
    print("Event keys:")
    print(list(log[0][0].keys()))

def print_trace_and_event_count(log, log_df):
    print("\n 3 ____________________________________________________________ \n")
    print("Number of traces:", len(log))
    print("\n 4 ____________________________________________________________ \n")
    event_stream = stream_converter.apply(log, variant=stream_converter.Variants.TO_EVENT_STREAM)
    print("Number of events:", len(event_stream))

def print_event_names(log_df):
    print("\n5.\n")
    events = log_df.drop_duplicates(subset='concept:name')
    print(events['concept:name'].tolist())

def print_start_end_activities(log):
    print("\n 6 ____________________________________________________________ \n")
    print("Start activities: ", pm4py.get_start_activities(log))
    print("End activities: ", pm4py.get_end_activities(log))

def print_event_array(log_df):
    print("\n 7 ____________________________________________________________ \n")
    print(log_df[['case:concept:name', 'concept:name', 'lifecycle:transition', 'time:timestamp']])

def filter_traces_ending_with_end(log):
    print("\n 8 Filtering ... \n")
    print("\n ____________________________________________________________\n")
    return pm4py.filter_end_activities(log, ["End"])

def apply_discovery_algorithms(log, filtered_log):
    print("\n 9 Discovery... \n")
    print("\n ____________________________________________________________\n")
    # Alpha Miner
    a_net, a_initial_marking, a_final_marking = alpha_miner.apply(log)
    af_net, af_initial_marking, af_final_marking = alpha_miner.apply(filtered_log)

    # Heuristics Miner
    h_net, h_initial_marking, h_final_marking = heuristics_miner.apply(log)
    hf_net, hf_initial_marking, hf_final_marking = heuristics_miner.apply(filtered_log)

    # Inductive Miner
    i_net = inductive_miner.apply(log)
    if_net = inductive_miner.apply(filtered_log)

    # Convert to PetriNet
    i_net, i_initial_marking, i_final_marking = pm4py.convert_to_petri_net(i_net)
    if_net, if_initial_marking, if_final_marking = pm4py.convert_to_petri_net(if_net)

    return {
        "alpha": (a_net, a_initial_marking, a_final_marking),
        "alpha_filtered": (af_net, af_initial_marking, af_final_marking),
        "heuristics": (h_net, h_initial_marking, h_final_marking),
        "heuristics_filtered": (hf_net, hf_initial_marking, hf_final_marking),
        "inductive": (i_net, i_initial_marking, i_final_marking),
        "inductive_filtered": (if_net, if_initial_marking, if_final_marking),
    }

def visualize_models(models):
    af_net, af_initial_marking, af_final_marking = models["alpha_filtered"]
    hf_net, hf_initial_marking, hf_final_marking = models["heuristics_filtered"]
    if_net, if_initial_marking, if_final_marking = models["inductive_filtered"]

    af_gviz = pn_visualizer.apply(af_net, af_initial_marking, af_final_marking)
    pn_visualizer.view(af_gviz)

    hf_gviz = pn_visualizer.apply(hf_net, hf_initial_marking, hf_final_marking)
    pn_visualizer.view(hf_gviz)

    if_gviz = pn_visualizer.apply(if_net, if_initial_marking, if_final_marking)
    pn_visualizer.view(if_gviz)

def evaluate_models(log, filtered_log, models):
    # Inizio della valutazione

    print("\n 10 Evaluating...\n")
    print("\n ____________________________________________________________\n")

    # Risultati per ogni modello, suddivisi tra 'filtered' e 'non-filtered'
    print("Evaluating Alpha model:")
    result_alpha = evaluation.apply(log, *models["alpha"])
    print("\n")
    print("Result for Alpha (non-filtered):")
    pprint(result_alpha)

    print("\n ------------------------------------------------------------\n")

    print("\nEvaluating Alpha Filtered model:")
    result_alpha_filtered = evaluation.apply(filtered_log, *models["alpha_filtered"])
    print("\n")
    print("Result for Alpha (filtered):")
    pprint(result_alpha_filtered)

    print("\n ------------------------------------------------------------\n")
    
    print("\nEvaluating Heuristics model:")
    result_heuristics = evaluation.apply(log, *models["heuristics"])
    print("\n")
    print("Result for Heuristics (non-filtered):")
    pprint(result_heuristics)

    print("\n ------------------------------------------------------------\n")
    
    print("\nEvaluating Heuristics Filtered model:")
    result_heuristics_filtered = evaluation.apply(filtered_log, *models["heuristics_filtered"])
    print("\n")
    print("Result for Heuristics (filtered):")
    pprint(result_heuristics_filtered)

    print("\n ------------------------------------------------------------\n")
    
    print("\nEvaluating Inductive model:")
    result_inductive = evaluation.apply(log, *models["inductive"])
    print("\n")
    print("Result for Inductive (non-filtered):")
    pprint(result_inductive)

    print("\n ------------------------------------------------------------\n")
    
    print("\nEvaluating Inductive Filtered model:")
    result_inductive_filtered = evaluation.apply(filtered_log, *models["inductive_filtered"])
    print("\n")
    print("Result for Inductive (filtered):")
    pprint(result_inductive_filtered)


def check_conformance(filtered_log, hf_net, hf_initial_marking, hf_final_marking):
    print("\n 11 ____________________________________________________________ \n")
    replayed_traces = token_replay.apply(filtered_log, hf_net, hf_initial_marking, hf_final_marking)

    num_not_fit = sum(1 for trace in replayed_traces if not trace['trace_is_fit'])
    print("Number of traces not fit: ", num_not_fit)

def main():
    # Define file path
    file_path = os.path.join(os.path.dirname(__file__), "dataset.xes")

    # 1. Load event log
    log, log_df = load_event_log(file_path)

    # 2. Print trace and event structure
    print_trace_and_event_structure(log)

    # 3 & 4. Print trace and event count
    print_trace_and_event_count(log, log_df)

    # 5. Print event names
    print_event_names(log_df)

    # 6. Print start and end activities
    print_start_end_activities(log)

    # 7. Print event array
    print_event_array(log_df)

    # 8. Filter traces ending with 'End'
    filtered_log = filter_traces_ending_with_end(log)

    # 9. Apply discovery algorithms
    models = apply_discovery_algorithms(log, filtered_log)

    # 10. Visualize models
    visualize_models(models)

    # 11. Evaluate models
    evaluate_models(log, filtered_log, models)

    # 12. Check conformance
    check_conformance(filtered_log, *models["inductive_filtered"])

if __name__ == "__main__":
    main()
