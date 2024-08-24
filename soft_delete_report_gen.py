
import subprocess 
import json
import datetime
from fpdf import FPDF



timestamp = datetime.datetime.now()
formatted_timestamp = timestamp.strftime("%Y-%m-%d %H%M%S")

pdf = FPDF() 
pdf.add_page()
pdf.set_font("Arial", size=8)
def add_to_pdf(text):
    pdf.cell(20, 4, txt=text, ln=True)

intro_text = "Buckets Soft Delete Retention Duration Inventory Report\n==================="

print(intro_text)
add_to_pdf(intro_text)


# Get all Projects
def list_all_gcp_projects(): 
    result = subprocess.run(['gcloud', 'projects', 'list', '--format=json"],
    stdout=subprocess.PIPE,
    text=True
    )
    projects = json.loads(result.stdout)
    return [project['projectId'] for project in projects]



# Get Buckets in Project
def list_buckets_in_project(project_id):
    result = subprocess.run(
        ['gcloud', 'storage', 'buckets', 'list', '--project', project_id, '--format=json'],
        stdout=subprocess.PIPE,
        text=True
    )
    if result.stdout.strip(): #check if project has buckets
    buckets = json.loads(result.stdout)
    return [bucket['name'] for bucket in buckets]
    return[]


# Get Bucket retention policy
def get_bucket_retention_policy (project_id, bucket_name):
    full_bucket_name = f"gs://{bucket_name}" #adding gs:// to the bucket name
    result = subprocess.run(
        ['gcloud', 'storage', 'buckets', 'describe', full_bucket_name, '--project', project_id, '--format=json'], 
    stdout=subprocess.PIPE,
    text=True
    )
    bucket_info = json.loads(result.stdout)
    soft_delete_policy = bucket_info.get('soft_delete_policy', {})
    retention_duration_seconds = soft_delete_policy.get('retentionDurationSeconds', 'No Soft Delete Policy')
    return retention_duration_seconds




def main():
    projects =list_all_gcp_projects()
    all_buckets = {}

    for project_id in projects:
        buckets = list_buckets_in_project(project_id)
        if buckets:
            all_buckets[project_id] = buckets
    # Print the results
    for project_id, buckets in all buckets.items():
        current_project = "Project: " + project_id
        print("==========")
        print(current_project)
        print("‒‒‒‒‒‒‒‒‒‒")
        add_to_pdf("==========
        add_to_pdf(current_project)
        add_to_pdf("‒‒‒‒‒‒‒‒‒‒")
        for bucket in buckets:
            retention_duration_seconds = get_bucket_retention_policy (project_id, bucket)
            retention_duration_days int(retention_duration_seconds)/86400 #converting retention duration from seconds to days current_bucket = " - Bucket: " + bucket + ", Soft Delete:" + str(retention_duration_days) + days" print(current_bucket)
            current_bucket = "    -Bucket: " + bucket + ",          Soft Delete: " + str(retention_duration_days) + " days"
            print(current_bucket)
            add_to_pdf(current_bucket)


if __name__ = "__main__":
    main()
    
    pdf.output("Buckets SoftDeletePolicyReport" + str(formatted_timestamp) + ".pdf")
    print("PDF File:  Buckets SoftDeletePolicyReport" + str(formatted_timestamp) + ".pdf)"