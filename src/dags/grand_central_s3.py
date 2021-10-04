import ast
import os
import shutil
import tempfile
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.email import send_email as SendEmail
from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook

from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule

## Notify

def on_failure_callback(context):
    payload = {'blocks': [{'type': 'section', 'text': {'type': 'mrkdwn', 'text': ''}}]}
    payload['blocks'][0]['text']['text'] = """
                :red_circle: Task Failed. 
                *Task*: {task}  
                *Dag*: {dag} 
                *Execution Time*: {exec_date}  
                *Log Url*: {log_url} 
                *Exception*: {exception} 
                """.format(
        task=context.get('task_instance').task_id,
        dag=context.get('task_instance').dag_id,
        ti=context.get('task_instance'),
        exec_date=context.get('execution_date'),
        log_url=context.get('task_instance').log_url,
        exception=context.get('exception'))

    #hook = SlackWebhookHook(http_conn_id='slack_notify_url', blocks=payload['blocks'])
    #hook.execute()


def create_temp_dir(**kwargs):
    return tempfile.mkdtemp()


def delete_temp_objects(zip_file_dict, path, **kwargs):
    if path and os.path.isdir(path):
        shutil.rmtree(path)
    if zip_file_dict.values():
        for values in zip_file_dict.values():
            for value in values:
                os.unlink(value)


def send_emails(target_files, config, **kwargs):
    config_obj = ast.literal_eval(config)
    for target in config_obj:
        SendEmail(
            to=target['target_list'],
            subject=target.get('subject'),
            html_content=target.get('html_content'),
            files=target_files[','.join(target['target_list'])],
        )


with DAG(
    dag_id='slack_and_email',
    start_date=days_ago(1),
    schedule_interval=None,
    tags=['Teste email Slack'],
    default_args={
        'on_failure_callback': on_failure_callback
    },
    params={"bucket": "", "config": [{"target_list": [], "subject": "", "html_content": "", "files": []}]},
) as dag:
    """
    Dag to send emails
    """

    start = DummyOperator(task_id='start')

    config = "{{dag_run.conf['config']}}"

    create_temp = PythonOperator(task_id='create_temp_dir', python_callable=create_temp_dir)

    delete_temp = PythonOperator(task_id='delete_temp_dir', python_callable=delete_temp_objects,
                                 op_kwargs={'path': create_temp.output, 'zip_file_dict': ''},
                                 trigger_rule=TriggerRule.NONE_FAILED)

    send_email = PythonOperator(task_id='send_emails', python_callable=send_emails,
                                op_kwargs={'config': config, "target_files": ''})

    finish = DummyOperator(task_id='finish', trigger_rule=TriggerRule.NONE_FAILED)

    start >> create_temp >> delete_temp >> send_email >> finish


