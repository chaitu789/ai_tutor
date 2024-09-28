from huggingface_hub import HfApi, HfFolder, Repository
import streamlit as st
import os

HF_API_TOKEN = "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"

def upload_files_to_hf_repo(uploaded_files, repo_id):
    hf_api = HfApi()
    file_paths = []
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            file_path = os.path.join(os.getcwd(), uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            hf_api.upload_file(
                path_or_fileobj=file_path,
                path_in_repo=uploaded_file.name,
                repo_id=repo_id,
                repo_type="dataset"
            )
            file_paths.append(file_path)

    return file_paths


def attach_files_to_assistant(assistant_model, file_paths):
    attached_files = []

    for file_path in file_paths:
        attached_files.append({"file_path": file_path})

    return attached_files
def check_and_upload_files(assistant_model, repo_id):

    st.warning("No Files Included, Upload Educational Material")
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

    if st.button("Upload and Attach Files"):
        if uploaded_files:
            try:
                file_paths = upload_files_to_hf_repo(uploaded_files, repo_id)


                attached_files_info = attach_files_to_assistant(assistant_model, file_paths)

                if not attached_files_info:
                    st.warning("No files were attached. Loading default data...")
                else:
                    st.success(f"{len(attached_files_info)} files successfully attached.")
            except Exception as e:
                st.error(f"An error occurred while attaching files: {e}")
        else:
            st.warning("Please select at least one file to upload.")
