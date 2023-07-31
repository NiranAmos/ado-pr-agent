import os
import openai
import difflib
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from costants import ProjectInfo
from azure.devops.v7_1.git.models import GitBaseVersionDescriptor


class AzureDevopsUtils:
    def __init__(self, connection):
        self._git_client = connection.clients.get_git_client()


    def get_repository_id(self, repository_name):
        # Get the list of repositories in the project
        repositories = self._git_client.get_repositories(project=project_name)

        # Find the repository by name and return its ID
        for repository in repositories:
            if repository.name == repository_name:
                return repository.id

        # Repository not found
        return None
    
    def send_message(self, messages, model_name, max_response_tokens=1500):
        response = openai.ChatCompletion.create(
            engine=model_name,
            messages=messages,
            temperature=0.5,
            max_tokens=max_response_tokens,
            top_p=0.9,
            frequency_penalty=0,
            presence_penalty=0)
        
        return response['choices'][0]['message']['content']
    
    
    def create_message_format(self, role,  content):
        return {"role": f"{role}", "content": content}
                    
    
    def init_agent(self, openai_api_key):
        openai.api_key = openai_api_key
        openai.api_base = "https://foundational-code-review.openai.azure.com/"
        openai.api_type = 'azure'
        openai.api_version = '2023-05-15'
        modelName = "niran-test"

        messages = [self.create_message_format("system", "You are world class code writer and your job is do code reviews.")]
        messages = [self.create_message_format("system", "I will send you a dictionary contains file name and list of changes and you will provide code review on each file. Ignore + or - characters in the changes list since it's part of git unified format. ")]

        return self.send_message(messages, modelName, 500)



organization_url = ProjectInfo.AZURE_DEVOPS_URI
personal_access_token = os.getenv("AZURE_DEVOPS_PAT")
project_name = ProjectInfo.AZURE_DEVOPS_PROJECT_NAME
repository_name = ProjectInfo.AZURE_DEVOPS_REPOSITORY_NAME
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=ProjectInfo.AZURE_DEVOPS_URI, creds=credentials)
azure_devops_utils = AzureDevopsUtils(connection)
repository_id = azure_devops_utils.get_repository_id(repository_name)
openai_api_key = os.getenv("OPENAI_API_KEY")
endpoint = ProjectInfo.AZURE_OPEN_AI_ENDPOINT
pull_request_id = ProjectInfo.PULL_REQUEST_ID

pull_request = azure_devops_utils._git_client.get_pull_request_by_id(pull_request_id, project_name)
source_branch = pull_request.source_ref_name.split('heads/')[-1]  
target_branch = pull_request.target_ref_name.split('heads/')[-1]  

base_descriptor = GitBaseVersionDescriptor(version_type='branch', version=source_branch)
target_descriptor = GitBaseVersionDescriptor(version_type='branch', version=target_branch)


commits = azure_devops_utils._git_client.get_pull_request_commits(repository_id ,pull_request_id, project_name)

changes_dict = {}

for commit in commits:
    changes = azure_devops_utils._git_client.get_changes(commit.commit_id, repository_id, project_name).changes
    for change in changes:
        if change['item']['gitObjectType'] == 'blob' and change['item']['path'].endswith('.cs'):
            path = change['item']['path']
            old_item = azure_devops_utils._git_client.get_item_content(repository_id, path, project_name, download = True, version_descriptor = target_descriptor)
            new_item = azure_devops_utils._git_client.get_item_content(repository_id, path, project_name, download = True, version_descriptor = base_descriptor)
            old_content = b''  
            new_content = b''  
            for chunk in old_item:  
                old_content += chunk  

            for chunk in new_item:  
                new_content += chunk  
  
            # Decode the byte string to a string using the file encoding  
            file_encoding = 'utf-8'
            old_content_decoded = old_content.decode(file_encoding)  
            new_content_decoded = new_content.decode(file_encoding)  
            diff = list(difflib.unified_diff(old_content_decoded.splitlines(), new_content_decoded.splitlines()))
    
            changes_list = []
            

            for line in diff:
                if not line.endswith('\n') and (line.startswith('+') or line.startswith('-')):
                    changes_list.append(line)

            changes_dict[path] = changes_list

response = azure_devops_utils.init_agent(openai_api_key)

response_list = []

for key in changes_dict:
    response_list.append(azure_devops_utils.send_message([azure_devops_utils.create_message_format("user", f"file name: {key}, changes: {changes_dict[key]}")], "niran-test"))


for response in response_list:
    print(response)