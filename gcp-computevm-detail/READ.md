This script lists out all the Compute instances details running on your Googcle Cloud Platform project such as , instance name , machine details , disks associated with it etc.

Requires python oauth2client : https://pypi.python.org/pypi/oauth2client  and and  googleapiclient : https://pypi.python.org/pypi/google-api-python-client/ packages
Download the Service Account file in JSON format from your GCP Console under : https://console.cloud.google.com/iam-admin/serviceaccounts/project?project=<your-project-id> and save it on the machine(windows/linux)
The script asks for two inputs : Service Account JSON file path and your google project ID

