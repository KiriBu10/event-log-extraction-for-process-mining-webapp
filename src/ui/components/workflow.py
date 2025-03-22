

from langgraph.graph import Graph
import pandas as pd
import sqlite3
import re
from Levenshtein import distance

def extract_sql_statement(text):
    sql_pattern = re.compile(r"(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|GRANT|REVOKE|TRUNCATE|MERGE|CALL|EXPLAIN|SHOW|USE|IS|NOT|AND|NULL|UNION|ALL|WHERE|FROM)\b.*?;", re.IGNORECASE | re.DOTALL)
    match = sql_pattern.search(text)
    # If a match is found, return the matched string
    if match:
        return match.group(0)
    else:
        return text #"no sql query in agent response."    

# Calculate all similiarity measures
def dataframe_similarity(df1,df2):
    result_full = dataframe_similiarity_full(df1,df2)
    result_relax = dataframe_similarity_relaxed(df1,df2)
    result_textual = dataframe_similiarity_textual(df1,df2,0.75)

    return {'precision':round(result_full['precision'],3), 'recall':round(result_full['recall'],3), 'f1':round(result_full['f1'],3)
            ,'relaxed_precision':round(result_relax['precision'],3), 'relaxed_recall':round(result_relax['recall'],3), 'relaxed_f1':round(result_relax['f1'],3)
            ,'textual_precision':round(result_textual['precision'],3), 'textual_recall':round(result_textual['recall'],3), 'textual_f1':round(result_textual['f1'],3)
            }


##### Comparison based on all columns
def dataframe_similiarity_full(df1,df2):

   # Ensure both dataframes compare the same columns, sorted alphabetically
    if set(df1.columns) != set(df2.columns):
        return "Can't calculate Precision, Recall and F1. DataFrames must have the same columns"
     
    df1 = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
    df2 = df2.sort_values(by=list(df1.columns)).reset_index(drop=True)

    # Create tuples of the rows
    df1['combined'] = df1.apply(lambda row: tuple(row), axis=1)
    df2['combined'] = df2.apply(lambda row: tuple(row), axis=1)
    
    # Create sets of the tuple rows for fast comparison
    set_df1 = set(df1['combined'])
    set_df2 = set(df2['combined'])
    
    # True Positives (TP): Items in both sets
    tp = len(set_df1.intersection(set_df2))
    
    # False Positives (FP): Items in df1 but not in df2
    fp = len(set_df1 - set_df2)
    
    # False Negatives (FN): Items in df2 but not in df1
    fn = len(set_df2 - set_df1)
    
    # Calculating precision, recall, and F1-score
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {'precision':round(precision,3), 'recall':round(recall,3), 'f1':round(f1,3) }


##### Comparison based on all columns except activity_id
def dataframe_similarity_relaxed(df1, df2):
    
    # drop columns with activity_id
    df1=df1.drop(['activity_id'], axis=1)
    df2=df2.drop(['activity_id'], axis=1)

   # Ensure both dataframes compare the same columns, sorted alphabetically
    if set(df1.columns) != set(df2.columns):
        return "Can't calculate Precision, Recall and F1. DataFrames must have the same columns"

    df1 = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
    df2 = df2.sort_values(by=list(df1.columns)).reset_index(drop=True)
    
    # Create tuples of the rows
    df1['combined'] = df1.apply(lambda row: tuple(row), axis=1)
    df2['combined'] = df2.apply(lambda row: tuple(row), axis=1)
    
    # Create sets of the tuple rows for fast comparison
    set_df1 = set(df1['combined'])
    set_df2 = set(df2['combined'])
    
    # True Positives (TP): Items in both sets
    tp = len(set_df1.intersection(set_df2))
    
    # False Positives (FP): Items in df1 but not in df2
    fp = len(set_df1 - set_df2)
    
    # False Negatives (FN): Items in df2 but not in df1
    fn = len(set_df2 - set_df1)
    
    # Calculating precision, recall, and F1-score
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0    

    return {'precision':round(precision,3), 'recall':round(recall,3), 'f1':round(f1,3)}


##### Comparison based on all columns using Levenshtein distance
def dataframe_similiarity_textual(df1,df2, threshold=0.75):

   # Ensure both dataframes compare the same columns, sorted alphabetically
    if set(df1.columns) != set(df2.columns):
        return "Can't calculate Precision, Recall and F1. DataFrames must have the same columns"

    df1 = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
    df2 = df2.sort_values(by=list(df1.columns)).reset_index(drop=True)

    ##### Textual comparison based on all columns
    tp, fp, fn = 0, 0, 0

    df2.fillna("",inplace=True)

    labels = df1.apply(";".join, axis=1)
    preds = df2.apply(";".join, axis=1)

    for label in labels:
        similarity_list=[]
        for pred in preds:
            similarity_list.append(distance(label,pred)/max(len(label), len(pred)))
        similarity_score = 1 - min(similarity_list) 
        if similarity_score >= threshold:
            tp += 1
        else:
            fp += 1

    fn = max(len(labels),len(preds)) - tp

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0 

    return {'precision':round(precision,3), 'recall':round(recall,3), 'f1':round(f1,3)}

def run_query_and_return_df(path_to_db, query, params=None):
    """
    Executes a SQL query and returns the results as a pandas DataFrame.
    
    :param path_to_db: The path to the SQLite database file.
    :param query: The SQL query string to be executed.
    :param params: Optional parameters to be bound to the query. Defaults to None.
    :return: A pandas DataFrame containing the results of the query.
    """
    # Connect to the SQLite database
    with sqlite3.connect(path_to_db) as conn:
        # If params is None, pandas will execute the query without parameters
        df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df



def run_query(conn, query="SELECT * FROM eventlog"):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute(query)
    
    # Fetch column names
    column_names = [description[0] for description in cursor.description]
    
    # Fetch the data
    data = cursor.fetchall()
    tbl = [dict(zip(column_names, row)) for row in data]

    with sqlite3.connect('example.db') as conn:
        # If params is None, pandas will execute the query without parameters
        df = pd.read_sql_query(query, conn, params=False)
    return tbl, df



class SimpleApp():
    def __init__(self, conn,path_to_groud_truth_eventlog, llm_model):
        self.conn = conn
        self.llm_model = llm_model 
        self.path_to_groud_truth_eventlog=path_to_groud_truth_eventlog

    def get_sql_query(self, state):
        messages = state['messages']
        user_input = messages[-1]
        response = self.llm_model.invoke(user_input)
        #state['messages'].append(response.content) # appending AIMessage response to the AgentState
        state['agent_response']=response.content
        return state
    
    def run_sql_query(self, state):
        #messages = state['messages']
        #agent_response = messages[-1]
        # Make sure that only the SQL statement is extracted from the agent response
        agent_response=extract_sql_statement(state['agent_response'])
        #agent_response = 'SELECT * FROM "order" where "id"="o1"'
        try:
            df = run_query_and_return_df(path_to_db = 'example.db', query = agent_response)
            #tbl, df = run_query(conn = self.conn, query = agent_response)
            state['sqlexecuter'] = df
            state['agent_response']=agent_response
        except Exception as e:
            state['sqlexecuter'] = 'ERROR'
            state['agent_response']=agent_response
        return state
    
    def calculate_metrics(self, state):
        if type(state['sqlexecuter']) != str:
            try:
                df_true = pd.read_csv(self.path_to_groud_truth_eventlog, dtype='object')
                state['result'] = 'I compared the extracted eventlog with the ground truth eventlog. This are the results: ' + str(dataframe_similarity(df_true, state['sqlexecuter']))
            except:
                state['result'] = "This is the result eventlog: "
        else:
            state['result'] = "Hm, I'm sorry, i couldn't run your statement. Let's try another one. Check also the example prompts."
        return state
        
    
    def invoke(self, AgentState):
        workflow = Graph()
        # nodes
        workflow.add_node("agent", self.get_sql_query)
        workflow.add_node("sqlexecuter", self.run_sql_query)
        workflow.add_node("dfcomparator", self.calculate_metrics)
        # edges
        workflow.add_edge('agent', 'sqlexecuter')
        workflow.add_edge('sqlexecuter', 'dfcomparator')
        # entry, exit
        workflow.set_entry_point("agent")
        workflow.set_finish_point("dfcomparator")
        app = workflow.compile()
        app.invoke(AgentState)
        return AgentState
