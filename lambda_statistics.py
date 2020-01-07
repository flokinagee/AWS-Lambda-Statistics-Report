
import boto3
from datetime import datetime, timedelta

class Lambda_Statistics():
    # Class variable
    maxval = 0
    # next_token = ''
    starttime = datetime.utcnow() - timedelta(days=7)
    endtime = datetime.utcnow()

    # def __init__(self, client):
    #     self.client = self.create_handler()
    
    def create_handler(self, service):
        return boto3.client(service)
  
    def getmetricdata(self, **event):
        if event.get('NextToken') is None or event.get('NextToken') == '':
            return self.client.get_metric_data(MetricDataQueries = 
                event.get("MetricDataQueries"),
                StartTime=event.get("StartTime"),
                EndTime=event.get("EndTime"),
                MaxDatapoints=5000
                )
        else:
            return self.client.get_metric_data(MetricDataQueries = 
                event.get("MetricDataQueries"),
                StartTime=event.get("StartTime"),
                EndTime=event.get("EndTime"),
                NextToken=event.get("NextToken"),
                MaxDatapoints=5000
            )
    def list_functions(self):
        lambada_hd = self.create_handler('lambda')

        paginator = lambada_hd.get_paginator('list_functions')

        for page in paginator.paginate():
            for function_name in page['Functions']:
                yield function_name['FunctionName']

    def list_metrics(self):
        for lambda_function in self.list_functions(self):
            results = self.getmetricdata(
                MetricDataQueries=[
                    {
                        'Id': 'invocations',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/Lambda',
                                'MetricName': 'Invocations',
                                'Dimensions': [
                                    {
                                        'Name': 'FunctionName',
                                        'Value': lambda_function
                                    },
                                ]
                            },
                            'Period': 60,
                            'Stat': 'Sum',
                            'Unit': 'Count'
                        },
                        'Label': 'Invocations',
                        'ReturnData': True 
                    },
                    {
                        'Id': 'errors',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/Lambda',
                                'MetricName': 'Errors',
                                'Dimensions': [
                                    {
                                        'Name': 'FunctionName',
                                        'Value': lambda_function
                                    },
                                ]
                            },
                            'Period': 60,
                            'Stat': 'Sum',
                            'Unit': 'Count'
                        },
                        'Label': 'Errors',
                        'ReturnData': True
                    },
                    {
                        'Id': 'duration',
                        'MetricStat': {
                            'Metric': {
                                'Namespace': 'AWS/Lambda',
                                'MetricName': 'Duration',
                                'Dimensions': [
                                    {
                                        'Name': 'FunctionName',
                                        'Value': lambda_function
                                    },
                                ]
                            },
                            'Period': 60,
                            'Stat': 'Average',
                            'Unit': 'Milliseconds'
                        },
                        'Label': 'Duration',
                        'ReturnData': True
                    }
                ],
                StartTime=starttime,
                EndTime=endtime,
                ScanBy='TimestampDescending',
                NextToken = ''
            )
    def display_results(self):
        list_metrics = self.list_metrics()

        if list_metrics['MetricDataResults'][0]['Timestamps']:
            for i in range(len(list_metrics['MetricDataResults'][0]['Timestamps'])):
                print('{:<80} | {:<25} | {:>11.3f} | {:>14.2f} | {:>17.1f}'.format(
                    func_name['FunctionName'],
                    str(response['MetricDataResults'][0]['Timestamps'][i]), 
                    response['MetricDataResults'][0]['Values'][i],
                    response['MetricDataResults'][1]['Values'][i]/1000,
                    round(response['MetricDataResults'][0]['Values'][i]/60 *response['MetricDataResults'][1]['Values'][i]/1000)
                )
                )
        else:
            print('{:<80} | {:<25} | {:<11} | {:<14} | {:<17}'.format(func_name['FunctionName'],'No Data','','',''))



