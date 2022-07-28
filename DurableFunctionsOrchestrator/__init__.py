import azure.functions as func
import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    image_list = yield context.call_activity('GetFileList')

    tasks = []
    for image in image_list:
        tasks.append(context.call_activity('CheckCatImage', image))
    results = yield context.task_all(tasks)
    
    results = yield context.call_activity('AnalyzeResult', results)
    
    return results

main = df.Orchestrator.create(orchestrator_function)