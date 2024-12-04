
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import openai
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests  # For making REST API calls


# Load the .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")



# Firebase REST API endpoints
FIREBASE_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
FIREBASE_LOGIN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

# Page configuration
st.set_page_config(
    page_title="RAG Enhanced Presentation Platform (REPP)",
    page_icon="📘",
    layout="wide"
)


# Custom CSS for animations and styling
st.markdown(
    """
    <style>
    /* General page styling */
    body {
        background-color: #f4f4f4; /* Light background color */
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
    }

    /* Logo styling */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
        animation: fadeIn 2s ease-in-out;
    }

    .logo {
        max-width: 200px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        animation: slideDown 2s ease-out;
    }

    /* Heading styling */
    .title-container {
        text-align: center;
        margin: 20px auto;
        color: #2a9df4;
        animation: slideDown 2s ease-out;
    }

    h1 {
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        margin: 10px auto;
    }

    /* Login box styling */
    .login-box {
        max-width: 400px;
        margin: 20px auto; /* Centered and reduced spacing */
        padding: 20px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        animation: fadeInUp 1s ease-in-out;
    }

    /* Remove margin issue for extra spacing */
    .login-box input {
        margin: 10px 0; /* Adds consistent spacing between input fields */
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }

    /* Button styling */
    .login-box button {
        background-color: #2a9df4;
        color: white;
        border: none;
        padding: 10px 15px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .login-box button:hover {
        background-color: #1b7ec6;
    }

    /* Animation keyframes */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes slideDown {
        from {
            transform: translateY(-50px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }

    @keyframes fadeInUp {
        from {
            transform: translateY(50px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)




# Login or Signup
def login_page():
    # Display the logo and title
    st.image("logo.png", width=350)

    st.markdown(
        """
        <div class="title-container" style="text-align: center;">
            <h1>Welcome to REPP</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
 
    # Login or Signup logic
    choice = st.selectbox('Login/Signup', ['Login', 'Signup'])

    if choice == 'Login':
       
        email = st.text_input('Email Address', key="login_email")
        password = st.text_input('Password', type='password', key="login_password")

        if st.button('Login'):
            if email and password:
                # Call Firebase REST API for Login
                payload = {
                    "email": email,
                    "password": password,
                    "returnSecureToken": True
                }
                response = requests.post(FIREBASE_LOGIN_URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Welcome back, {data['email']}!")
                    st.session_state['logged_in'] = True
                else:
                    error_message = response.json().get("error", {}).get("message", "An error occurred")
                    st.error(f"Login failed: {error_message}")
            else:
                st.error("Please enter both email and password.")

    elif choice == 'Signup':
        st.markdown(
            """
            <div class="signup-box" style="text-align: center; padding: 20px; border: 1px solid #ccc; border-radius: 10px; background-color: #f9f9f9;">
            """,
            unsafe_allow_html=True
        )
        email = st.text_input('Email Address', key="signup_email")
        password = st.text_input('Password', type='password', key="signup_password")
        confirm_password = st.text_input('Confirm Password', type='password', key="signup_confirm_password")

        if st.button('Signup'):
            if password != confirm_password:
                st.error("Passwords do not match!")
            elif email and password:
                # Call Firebase REST API for Signup
                payload = {
                    "email": email,
                    "password": password,
                    "returnSecureToken": True
                }
                response = requests.post(FIREBASE_SIGNUP_URL, json=payload)
                if response.status_code == 200:
                    st.success("Signup successful! Please login using your credentials.")
                    st.balloons()
                else:
                    error_message = response.json().get("error", {}).get("message", "An error occurred")
                    st.error(f"Signup failed: {error_message}")
            else:
                st.error("Please fill in all fields.")

# Check login status
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Show login page if not logged in
if not st.session_state['logged_in']:
    login_page()
    st.stop()








  


# CSS 
st.markdown("""
    <style>
    /* General App Styling */
    .stApp {
        background-color: #fffacd; /* Bright yellow background */
        color: red; /* Red text for overall content */
        font-family: 'Arial', sans-serif; /* Modern font */
        font-size: 16px; /* Base font size */
        line-height: 1.6;
        margin: 0 auto;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* Soft shadow effect */
    }

    /* Header Section */
    h1, h2, h3, h4, h5, h6 {
        color: red; /* Bold red for headings */
        text-align: center; /* Center align all headings */
        font-family: 'Comic Sans MS', cursive; /* Fancy font for headings */
        margin-bottom: 20px;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #ffd700 !important; /* Golden yellow for sidebar */
        color: red !important; /* Red text for sidebar */
        border-right: 3px solid red; /* Fancy sidebar border */
    }

    /* Buttons */
    .stButton button {
        background-color: #ff4500; /* Orange-red buttons */
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 12px;
        border: 2px solid white;
        box-shadow: 2px 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #ff6347; /* Tomato color on hover */
        color: yellow;
        transform: scale(1.05); /* Slight grow effect */
    }

    /* Inputs */
    .stTextInput > div > input, .stTextArea > div > textarea {
        background-color: #fffacd !important; /* Light yellow input background */
        color: red !important; /* Red text */
        border: 2px solid red !important; /* Red borders */
        border-radius: 10px; /* Rounded inputs */
        padding: 10px; /* Padding for comfort */
        font-size: 16px;
    }

    /* Expanders */
    .st-expander {
        background-color: #fffacd !important;
        border: 2px solid red !important; /* Red border for expanders */
        border-radius: 10px !important;
    }
    .st-expander > div > div {
        color: red !important; /* Red text in expanders */
    }

    /* Footer */
    .footer-container {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #ffd700; /* Golden yellow footer */
        text-align: center;
        padding: 10px 0;
        border-top: 3px solid red;
    }
    .footer-container h6 {
        color: red;
        font-family: 'Arial', sans-serif;
        margin: 0;
        font-size: 14px;
    }

    /* Miscellaneous */
    .stMarkdown div {
        color: red !important; /* Force red text in Markdown */
    }
    .stDataFrame {
        border: 2px solid red; /* Add fancy border to tables */
    }
    </style>
""", unsafe_allow_html=True)



# Sidebar Navigation with dynamic visibility of "REPP"
# Define the list of pages
pages = ["Home", "Dashboards and Datasets", "Presentation", "Query Assistant", "Contact the Creator"]

# Insert "REPP" as the first page if customization is not done
if not st.session_state.get('customization_done', False):  # Default to False if not set
    pages.insert(0, "REPP")

# Initialize current page in session state
if "current_page" not in st.session_state:
    st.session_state["current_page"] = pages[0]  # Default to the first page

# Callback function to update current page in session state
def update_page():
    st.session_state["current_page"] = st.session_state["selected_page"]

# Display the logo at the top of the sidebar
st.sidebar.image("logo.png", use_column_width=True)


# Sidebar radio button with dynamic selection
st.sidebar.radio(
    "Go to", 
    options=pages, 
    index=pages.index(st.session_state["current_page"]), 
    key="selected_page", 
    on_change=update_page  # Update the page on selection
)

# Add a Logout Button to the Sidebar
if st.session_state.get("logged_in", False):
    if st.sidebar.button("Logout", key="logout_button", help="Click to logout"):
        # Reset the login state
        st.session_state["logged_in"] = False
        st.session_state["current_page"] = "Home"  # Redirect to Home or Login
        st.success("You have been logged out.")
        st.stop()

# Synchronize the `page` variable with the session state
page = st.session_state["current_page"]




# Sidebar Explanation
if page == "REPP":
    st.sidebar.markdown("Welcome to the customization page of REPP! Here, you can personalize the content and styling of your presentation.")
elif page == "Home":
    st.sidebar.markdown("The Home page displays customized details like the project name, team members, and supervisor in your chosen style.")
elif page == "Dashboards and Datasets":
    st.sidebar.markdown("This page allows you to upload and download dashboards and datasets relevant to your project.")
elif page == "Presentation":
    st.sidebar.markdown("The Presentation page lets you share a slideshow for your project using Google Slides.")
elif page == "Query Assistant":
    st.sidebar.markdown("The Query Assistant allows you to upload a PDF and interact with it using AI.")


# Initialize session states for dynamic updates
# Initialize session states
if "current_question" not in st.session_state:
    st.session_state["current_question"] = ""

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "REPP"

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if 'project_data' not in st.session_state:
    st.session_state['project_data'] = {
        "name": "",
        "team": "",
        "supervisor": "",
        "pdf": None,
        "dashboards": [],
        "datasets": [],
        "presentation": None,
        "details": "",
        "images": [],
        "google_slides": "",
        "custom_text_name": {  
            "content": "",
            "font_size": 16,
            "is_bold": False,
            "is_italic": False,
            "color": "#000000"
        },
        "custom_text_team": {
            "content": "",
            "font_size": 16,
            "is_bold": False,
            "is_italic": False,
            "color": "#000000"
        },
        "custom_text_supervisor": {
            "content": "",
            "font_size": 16,
            "is_bold": False,
            "is_italic": False,
            "color": "#000000"
        },
        "custom_text_details": {
            "content": "",
            "font_size": 16,
            "is_bold": False,
            "is_italic": False,
            "color": "#000000"
        }
    }


# Input Page: Add customization options for each section
if page == "REPP":
    st.title("Welcome to the customization page of the RAG Enhanced Presentation Platform (REPP)")
    st.markdown("""
    <div style="text-align: center; color: grey; font-size: 14px; font-family: Arial, sans-serif; margin-top: 20px;">
        © 2024 Syed Faizan. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

    # Available fonts
    available_fonts = ["Arial", "Comic Sans MS", "Courier New", "Georgia", "Times New Roman", "Verdana", "Tahoma"]

    # Project Name Section
    with st.expander("Customize Project Name Section"):
        st.text_area(
            "Project Name Content",
            value=st.session_state['project_data']["custom_text_name"]["content"],
            key="custom_text_name_content"
        )
        st.slider(
            "Font Size",
            10, 30,
            value=st.session_state['project_data']["custom_text_name"]["font_size"],
            key="custom_text_name_font_size"
        )
        st.color_picker(
            "Text Color",
            value=st.session_state['project_data']["custom_text_name"]["color"],
            key="custom_text_name_color"
        )
        st.selectbox(
            "Font Family",
            options=available_fonts,
            index=available_fonts.index(st.session_state['project_data']["custom_text_name"].get("font", "Arial")),
            key="custom_text_name_font"
        )
        st.checkbox(
            "Bold",
            value=st.session_state['project_data']["custom_text_name"]["is_bold"],
            key="custom_text_name_is_bold"
        )
        st.checkbox(
            "Italic",
            value=st.session_state['project_data']["custom_text_name"]["is_italic"],
            key="custom_text_name_is_italic"
        )

    # Similar customization for Team Members Section
    with st.expander("Customize Team Members Section"):
        st.text_area(
            "Team Members Content",
            value=st.session_state['project_data']["custom_text_team"]["content"],
            key="custom_text_team_content"
        )
        st.slider(
            "Font Size",
            10, 30,
            value=st.session_state['project_data']["custom_text_team"]["font_size"],
            key="custom_text_team_font_size"
        )
        st.color_picker(
            "Text Color",
            value=st.session_state['project_data']["custom_text_team"]["color"],
            key="custom_text_team_color"
        )
        st.selectbox(
            "Font Family",
            options=available_fonts,
            index=available_fonts.index(st.session_state['project_data']["custom_text_team"].get("font", "Arial")),
            key="custom_text_team_font"
        )
        st.checkbox(
            "Bold",
            value=st.session_state['project_data']["custom_text_team"]["is_bold"],
            key="custom_text_team_is_bold"
        )
        st.checkbox(
            "Italic",
            value=st.session_state['project_data']["custom_text_team"]["is_italic"],
            key="custom_text_team_is_italic"
        )

    # Similar sections for Supervisor and Project Details
    with st.expander("Customize Supervisor Section"):
        st.text_area(
            "Supervisor Content",
            value=st.session_state['project_data']["custom_text_supervisor"]["content"],
            key="custom_text_supervisor_content"
        )
        st.slider(
            "Font Size",
            10, 30,
            value=st.session_state['project_data']["custom_text_supervisor"]["font_size"],
            key="custom_text_supervisor_font_size"
        )
        st.color_picker(
            "Text Color",
            value=st.session_state['project_data']["custom_text_supervisor"]["color"],
            key="custom_text_supervisor_color"
        )
        st.selectbox(
            "Font Family",
            options=available_fonts,
            index=available_fonts.index(st.session_state['project_data']["custom_text_supervisor"].get("font", "Arial")),
            key="custom_text_supervisor_font"
        )
        st.checkbox(
            "Bold",
            value=st.session_state['project_data']["custom_text_supervisor"]["is_bold"],
            key="custom_text_supervisor_is_bold"
        )
        st.checkbox(
            "Italic",
            value=st.session_state['project_data']["custom_text_supervisor"]["is_italic"],
            key="custom_text_supervisor_is_italic"
        )

    with st.expander("Customize Project Details Section"):
        st.text_area(
            "Project Details Content",
            value=st.session_state['project_data']["custom_text_details"]["content"],
            key="custom_text_details_content"
        )
        st.slider(
            "Font Size",
            10, 30,
            value=st.session_state['project_data']["custom_text_details"]["font_size"],
            key="custom_text_details_font_size"
        )
        st.color_picker(
            "Text Color",
            value=st.session_state['project_data']["custom_text_details"]["color"],
            key="custom_text_details_color"
        )
        st.selectbox(
            "Font Family",
            options=available_fonts,
            index=available_fonts.index(st.session_state['project_data']["custom_text_details"].get("font", "Arial")),
            key="custom_text_details_font"
        )
        st.checkbox(
            "Bold",
            value=st.session_state['project_data']["custom_text_details"]["is_bold"],
            key="custom_text_details_is_bold"
        )
        st.checkbox(
            "Italic",
            value=st.session_state['project_data']["custom_text_details"]["is_italic"],
            key="custom_text_details_is_italic"
        )


    # Save Changes Button
    if st.button("Save Changes"):
        st.session_state['project_data']["custom_text_name"].update({
            "content": st.session_state.custom_text_name_content,
            "font_size": st.session_state.custom_text_name_font_size,
            "color": st.session_state.custom_text_name_color,
            "font": st.session_state.custom_text_name_font,
            "is_bold": st.session_state.custom_text_name_is_bold,
            "is_italic": st.session_state.custom_text_name_is_italic,
        })
        st.session_state['project_data']["custom_text_team"].update({
            "content": st.session_state.custom_text_team_content,
            "font_size": st.session_state.custom_text_team_font_size,
            "color": st.session_state.custom_text_team_color,
            "font": st.session_state.custom_text_team_font,
            "is_bold": st.session_state.custom_text_team_is_bold,
            "is_italic": st.session_state.custom_text_team_is_italic,
        })
        st.session_state['project_data']["custom_text_supervisor"].update({
            "content": st.session_state.custom_text_supervisor_content,
            "font_size": st.session_state.custom_text_supervisor_font_size,
            "color": st.session_state.custom_text_supervisor_color,
            "font": st.session_state.custom_text_supervisor_font,
            "is_bold": st.session_state.custom_text_supervisor_is_bold,
            "is_italic": st.session_state.custom_text_supervisor_is_italic,
        })
        st.session_state['project_data']["custom_text_details"].update({
            "content": st.session_state.custom_text_details_content,
            "font_size": st.session_state.custom_text_details_font_size,
            "color": st.session_state.custom_text_details_color,
            "font": st.session_state.custom_text_details_font,
            "is_bold": st.session_state.custom_text_details_is_bold,
            "is_italic": st.session_state.custom_text_details_is_italic,
        })

        st.success("Changes saved successfully!")


        # Dashboards Upload Section
    st.subheader("Upload Dashboards")
    uploaded_dashboards = st.file_uploader(
            "Upload your dashboards (Power BI, Tableau, etc.)", 
            type=["pbix", "twb", "twbx"], 
            accept_multiple_files=True,
            key="dashboard_upload"
        )
    if uploaded_dashboards:
        if "dashboards" not in st.session_state['project_data']:
                st.session_state['project_data']["dashboards"] = []
        st.session_state['project_data']["dashboards"].extend(uploaded_dashboards)
        st.success(f"{len(uploaded_dashboards)} dashboard(s) uploaded successfully!")

        # Datasets Upload Section
    st.subheader("Upload Datasets")
    uploaded_datasets = st.file_uploader(
            "Upload your datasets (CSV, Excel, etc.)", 
            type=["csv", "xls", "xlsx"], 
            accept_multiple_files=True,
            key="dataset_upload"
        )
    if uploaded_datasets:
        if "datasets" not in st.session_state['project_data']:
            st.session_state['project_data']["datasets"] = []
        st.session_state['project_data']["datasets"].extend(uploaded_datasets)
        st.success(f"{len(uploaded_datasets)} dataset(s) uploaded successfully!")

        # Presentation Upload Section
    st.subheader("Upload Presentation")
    uploaded_presentations = st.file_uploader(
            "Upload your presentations (PPT, PPTX)", 
            type=["ppt", "pptx"], 
            accept_multiple_files=True,
            key="presentation_upload"
        )
    if uploaded_presentations:
        if "presentations" not in st.session_state['project_data']:
            st.session_state['project_data']["presentations"] = []
        st.session_state['project_data']["presentations"].extend(uploaded_presentations)
        st.success(f"{len(uploaded_presentations)} presentation(s) uploaded successfully!")

        # Google Slides Link
    st.subheader("Embed Google Slides")
    google_slides_link = st.text_input(
            "Paste the link to your Google Slides presentation",
            value=st.session_state['project_data'].get("google_slides", ""),
            key="google_slides_link"
        )
    if google_slides_link:
            st.session_state['project_data']["google_slides"] = google_slides_link
            st.success("Google Slides link saved successfully!")

        # Images Upload Section
    st.subheader("Upload Images for a home page Gallery")
    uploaded_images = st.file_uploader(
            "Upload images for the home page (JPEG, PNG)", 
            type=["jpg", "jpeg", "png"], 
            accept_multiple_files=True,
            key="image_upload"
        )
    if uploaded_images:
        if "images" not in st.session_state['project_data']:
                st.session_state['project_data']["images"] = []
        st.session_state['project_data']["images"].extend(uploaded_images)
        st.success(f"{len(uploaded_images)} image(s) uploaded successfully!")







# Home Page: Apply customizations to each section
elif page == "Home":
    # Project Name Section
    project_name_custom = st.session_state['project_data']["custom_text_name"]
    st.markdown(f"""
        <h1 style="font-size:{project_name_custom['font_size']}px; color:{project_name_custom['color']}; font-weight:{'bold' if project_name_custom['is_bold'] else 'normal'}; font-style:{'italic' if project_name_custom['is_italic'] else 'normal'}; font-family:{project_name_custom.get('font', 'Arial')}; text-align:center;">
            {project_name_custom['content']}
        </h1>
    """, unsafe_allow_html=True)

    # Team Members Section
    team_custom = st.session_state['project_data']["custom_text_team"]
    st.subheader("Team Members")
    st.markdown(f"""
        <div style="font-size:{team_custom['font_size']}px; color:{team_custom['color']}; font-weight:{'bold' if team_custom['is_bold'] else 'normal'}; font-style:{'italic' if team_custom['is_italic'] else 'normal'}; font-family:{team_custom.get('font', 'Arial')};">
            {team_custom['content']}
        </div>
    """, unsafe_allow_html=True)

        # Supervisor Section
    st.subheader("Supervisor")
    supervisor_custom = st.session_state['project_data']["custom_text_supervisor"]
    st.markdown(f"""
        <div style="font-size:{supervisor_custom['font_size']}px; color:{supervisor_custom['color']}; font-weight:{'bold' if supervisor_custom['is_bold'] else 'normal'}; font-style:{'italic' if supervisor_custom['is_italic'] else 'normal'}; font-family:{supervisor_custom.get('font', 'Arial')};">
            {supervisor_custom['content']}
        </div>
    """, unsafe_allow_html=True)

    # Project Details Section
    st.subheader("Project Details")
    details_custom = st.session_state['project_data']["custom_text_details"]
    st.markdown(f"""
        <div style="font-size:{details_custom['font_size']}px; color:{details_custom['color']}; font-weight:{'bold' if details_custom['is_bold'] else 'normal'}; font-style:{'italic' if details_custom['is_italic'] else 'normal'}; font-family:{details_custom.get('font', 'Arial')};">
            {details_custom['content']}
        </div>
    """, unsafe_allow_html=True)

    # Display Uploaded Images
    st.subheader("Gallery")
    images = st.session_state['project_data'].get("images", [])
    if images:
        for image in images:
            st.image(image, caption=image.name, use_container_width=True)
    else:
        st.write("No images uploaded.")


    st.markdown("""
    <div style="text-align: center; color: grey; font-size: 14px; font-family: Arial, sans-serif; margin-top: 20px;">
        © 2024 Syed Faizan. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

elif page == "Dashboards and Datasets":
    st.title("Dashboards and Datasets")

    # Display Dashboards
        # Display uploaded dashboards
    st.subheader("Dashboards")
    dashboards = st.session_state['project_data'].get('dashboards', [])
    if dashboards:
        for i, dashboard in enumerate(dashboards):
            st.download_button(
                label=f"Download {dashboard.name}",
                data=dashboard,
                file_name=dashboard.name,
                key=f"download_dashboard_{i}"  # Unique key
            )
    else:
        st.write("No dashboards uploaded.")


    # Display Datasets
    st.subheader("Uploaded Datasets")
    datasets = st.session_state['project_data'].get("datasets", [])
    if datasets:
        for dataset in datasets:
            st.download_button(label=f"Download {dataset.name}", data=dataset, file_name=dataset.name)
    else:
        st.write("No datasets uploaded.")


elif page == "Presentation":
    st.title("Presentation")

    # Display Uploaded Presentations
    st.subheader("Uploaded Presentations")
    presentations = st.session_state['project_data'].get("presentations", [])
    if presentations:
        for presentation in presentations:
            st.download_button(label=f"Download {presentation.name}", data=presentation, file_name=presentation.name)
    else:
        st.write("No presentations uploaded.")

    # Display Embedded Google Slides
    st.subheader("Embedded Google Slides")
    google_slides = st.session_state['project_data'].get("google_slides", "")
    if google_slides:
        st.markdown(f"""
            <iframe src="{google_slides}" width="100%" height="600px" frameborder="0" allowfullscreen></iframe>
        """, unsafe_allow_html=True)
    else:
        st.write("No Google Slides link provided.")

    


elif page == "Query Assistant":
    st.title("Query Assistant")
    st.sidebar.title("RAG Chatbot")  # Keep Chatbot title on the sidebar only in this page

    # Sidebar instructions
    st.sidebar.markdown("""
    ### About the Query Assistant
    Upload a PDF and ask questions. This assistant uses retrieval-augmented generation (RAG) to provide accurate answers based on the uploaded document.
    
    #### 💡 Tips:
    To use the RAG-Based Report Query Assistant, the **"ASK"** button must be clicked twice:
    1. Once after entering the question in the input box.
    2. A second time after the **"Analyzing Sources"** message disappears.

    This ensures that the query is fully processed and returns accurate results.
    """)

    # Chat history initialization
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # File uploader for PDF
    pdf_file = st.file_uploader("Upload a PDF for Chatbot", type="pdf")
    if pdf_file:
        # Load and preprocess the PDF
        reader = PdfReader(pdf_file)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        cleaned_text = text.replace("\n", " ").strip()

        # Split text into chunks for vector storage
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(cleaned_text)

        # Generate embeddings and create FAISS index
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(chunks, embeddings)
        vector_store.save_local("uploaded_pdf")

        # RAG function
        def rag(query, n_results=5):
            docs = vector_store.similarity_search(query, k=n_results)
            joined_information = "\n".join([doc.page_content for doc in docs])

            # Use structured prompt
            prompt = f"""
            You are a knowledgeable assistant. Use the provided document context to answer the following question:
            Context: {joined_information}
            Question: {query}
            Answer concisely and accurately.
            """
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content, docs

            # Chat interface in container
        chat_container = st.container()

        with chat_container:
        # Display chat history
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"<div class='chat-message user-message'>💭 You: {message['content']}</div>", 
                        unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='chat-message assistant-message'>
                        <div style='margin-bottom: 0.5rem;'>📘 Assistant: {message['response']}</div>
                    </div>
                """, unsafe_allow_html=True)

    # If there's a current question in the session state, use it as the default value
        user_query = st.text_input(
            label="Ask your question about the uploaded document",
            help="Type your question or click an example below",
            placeholder="Example: What are the key trends discussed?",
            value=st.session_state.current_question,
            key="unique_user_input_key"  # Assign a unique key
        )

    # Query input with examples
        st.markdown("<div class='chat-input'>", unsafe_allow_html=True)


    # Example questions as buttons
        example_questions = [
            "What are the key findings?",
            "What are the important trends discussed?",
            "What are the recommendations in the document?",
            "What is the main topic of the document?"
        ]

        st.markdown("### 💡 Example Questions")
        cols = st.columns(2)
        for idx, question in enumerate(example_questions):
        # Assign a unique key for each button
            if cols[idx % 2].button(question, key=f"example_question_key_{idx}"):
                st.session_state.current_question = question  # Set the selected example question

    # Single "Ask" Button Logic
        if st.button("Ask", type="primary", use_container_width=True):  # Ensure only one button
            if not user_query:
                st.warning("⚠️ Please enter a question!")
            else:
            # Append user's query to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_query})
            
                with st.spinner("🔍 Analyzing sources..."):
                    try:
                    # Call the RAG function and get response and sources
                        response, sources = rag(user_query)
                    
                    # Append assistant's response to chat history
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "response": response,
                            "sources": sources
                        })
                    
                    # Clear the current question after processing
                        st.session_state.current_question = ''
                    
                    # Update app state to refresh UI
                        st.session_state['force_rerun'] = True  # Trigger UI update
                    except Exception as e:
                    # Log and display a detailed error message
                        st.error(f"⚠️ An error occurred while processing your query: {str(e)}")

    # Close the chat input container
        st.markdown("</div>", unsafe_allow_html=True)


                        # Clear chat history button
        if st.sidebar.button("Clear Chat History"):
            # Clear the chat history and reset current question
            st.session_state.chat_history = []
            st.session_state.current_question = ""  # Reset the input box
            st.rerun()  # Immediately refresh the app to reflect changes




st.markdown("""
    <div class="footer-container">
        <h3>© 2024 Syed Faizan. All rights reserved.</h3>
    </div>
""", unsafe_allow_html=True)


# Contact the Creator Page
if st.session_state['current_page'] == "Contact the Creator":
    st.title("Contact the Creator of REPP - Syed Faizan")
    
    st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <h3>Connect with Syed Faizan</h3>
        </div>
    """, unsafe_allow_html=True)

    # Social Media Links
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div style="text-align: center; margin: 10px;">
                <a href="mailto:faizan.s@northeastern.edu" target="_blank" style="text-decoration: none; font-size: 16px; color: #FF4500;">
                    📧 Email
                </a>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="text-align: center; margin: 10px;">
                <a href="https://www.linkedin.com/in/drsyedfaizanmd/" target="_blank" style="text-decoration: none; font-size: 16px; color: #0077B5;">
                    🔗 LinkedIn
                </a>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div style="text-align: center; margin: 10px;">
                <a href="https://github.com/SYEDFAIZAN1987" target="_blank" style="text-decoration: none; font-size: 16px; color: #333;">
                    🐙 GitHub
                </a>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <a href="https://twitter.com/faizan_data_ml" target="_blank" style="text-decoration: none; font-size: 16px; color: #1DA1F2;">
                🐦 Twitter
            </a>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div style="text-align: center; margin-top: 30px; color: grey; font-size: 14px;">
            © 2024 Syed Faizan. All rights reserved.
        </div>
    """, unsafe_allow_html=True)


