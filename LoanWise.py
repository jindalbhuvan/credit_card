import streamlit as st
import pandas as pd
import joblib
import base64
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import urllib.parse
from io import BytesIO

# Custom title with favicon
st.set_page_config(
    page_title="LoanWise - Smart Loan Recovery System",
    page_icon="💼",  
    layout="wide"
)

# Custom CSS for better text visibility and vibrant colors
st.markdown("""
    <style>
    /* Main title styling */
    .main-title {
        color: #FFFFFF;
        font-size: 48px;
        font-weight: bold;
        text-shadow: 2px 2px 4px #000000;
        text-align: center;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    /* Subheader styling */
    .custom-subheader {
        color: #FFD700;
        font-size: 28px;
        font-weight: bold;
        text-shadow: 1px 1px 2px #000000;
        padding: 5px;
        border-bottom: 2px solid #FFD700;
    }
    
    /* Content text styling */
    .content-text {
        color: #FFFFFF;
        font-size: 18px;
        background-color: rgba(0, 0, 0, 0.6);
        padding: 10px;
        border-radius: 5px;
    }
    
    /* Options styling */
    .option-label {
        font-weight: bold;
        color: #FF6B6B;
        font-size: 18px;
        background-color: rgba(255, 255, 255, 0.2);
        padding: 5px;
        border-radius: 5px;
    }
    
    /* Input field labels */
    .stNumberInput label, .stTextInput label, .stSelectbox label {
        color: #00FFFF !important;
        font-weight: bold !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 1px #000000;
    }
    
    /* Making radio buttons more visible */
    .stRadio label {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 18px !important;
        background-color: rgba(255,255,255,0.8);
        padding: 3px;
        border-radius: 5px;
    }
          
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
        color: white !important;  /* Ensure text remains visible */
        font-weight: bold;
        border: none;
        padding: 16px 55px;
        border-radius: 12px;
        box-shadow: 0 5px 10px rgba(255, 65, 108, 0.4);
        font-size: 18px;
        transition: all 0.3s ease-in-out;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Hover effect */
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(255, 65, 108, 0.6);
        background: linear-gradient(135deg, #FF4B2B 0%, #FF416C 100%);
        color: white !important; /* Keep text visible on hover */
    }

    /* Active effect (click effect) */
    .stButton button:active {
        transform: scale(0.95);
        box-shadow: 0 3px 5px rgba(255, 65, 108, 0.5);
        background: linear-gradient(135deg, #D33050 0%, #C72B40 100%);
        color: white !important; /* Keep text visible when clicked */
    }

    /* Dataframe styling */
    .dataframe {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #000000 !important;
        font-weight: bold !important;
    }
    
   /* Sidebar styling with blue to green gradient */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E3B70 0%, #107869 50%, #0F9B58 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Ensure all text in sidebar is white and visible */
    section[data-testid="stSidebar"] .css-1d391kg, 
    section[data-testid="stSidebar"] .css-1a1fmpi, 
    section[data-testid="stSidebar"] .css-1v0mbdj,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] span {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }

    /* Adding a subtle shadow to all sidebar elements for better visibility */
    section[data-testid="stSidebar"] > div {
        padding: 2rem 1rem;
    }

    /* Enhance sidebar welcome message */
    section[data-testid="stSidebar"] h3 {
        text-transform: uppercase;
        letter-spacing: 1px;
        background: rgba(255, 255, 255, 0.1);
        padding: 8px 15px;
        border-radius: 5px;
        margin-top: 15px;
    }
    
    /* Uniform button styling for sharing section */
    .uniform-button {
        background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
        color: white !important;
        font-weight: bold;
        border: none;
        padding: 12px 8px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        font-size: 16px;
        width: 100%;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        text-decoration: none;
        margin-bottom: 10px;
    }

    .uniform-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }

    .uniform-button.download {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    }

    .uniform-button.whatsapp {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
    }

    .uniform-button.telegram {
        background: linear-gradient(135deg, #0088cc 0%, #005577 100%);
    }

    .uniform-button.copy {
        background: linear-gradient(135deg, #FF9966 0%, #FF5E62 100%);
    }
            
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Animation class that can be applied to elements */
    .pulse-animation {
        animation: pulse 3s infinite;
    }
            
    .buttons-container {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        gap: 10px;
        flex-wrap: wrap;
    }

    @media (max-width: 768px) {
        .buttons-container {
            flex-direction: column;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Function to set local image as background
def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        /* Add a semi-transparent overlay for better text readability */
        .stApp:before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0);
            z-index: -1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Calling the function with the local image path
add_bg_from_local("background.jpg")

# Load pretrained model
rf_model = joblib.load('rf_model.pkl')

# Sample template data for bulk upload
sample_data = pd.DataFrame({
    'Customer_ID': [],
    'Age': [],
    'Monthly_Income': [],
    'Loan_Amount': [],
    'Loan_Tenure': [],
    'Interest_Rate': [],
    'Collateral_Value': [],
    'Outstanding_Loan_Amount': [],
    'Monthly_EMI': [],
    'Num_Missed_Payments': [],
    'Days_Past_Due': []
})

# Saving sample template with mandatory fields marked in red
sample_file_path = 'sample_template.xlsx'
with pd.ExcelWriter(sample_file_path, engine='xlsxwriter') as writer:
    sample_data.to_excel(writer, sheet_name='Template', index=False)
    workbook = writer.book
    worksheet = writer.sheets['Template']

    # Format for mandatory columns
    red_format = workbook.add_format({'bg_color': 'red', 'font_color': 'white'})

    # Apply red format to mandatory columns
    mandatory_columns = ['Age', 'Monthly_Income', 'Loan_Amount', 'Loan_Tenure', 'Interest_Rate']
    for col_num, col_name in enumerate(sample_data.columns):
        if col_name in mandatory_columns:
            worksheet.write(0, col_num, col_name, red_format)

# Function to upload file to Google Drive and generate shareable links
def get_shareable_links(file_path, file_name):
    try:
        # Authenticate with Google
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile("mycreds.txt")
        if gauth.credentials is None:
            # Authenticate if they're not available
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile("mycreds.txt")
        
        drive = GoogleDrive(gauth)
        
        # Check if we have previously uploaded a file with the same name
        # If so, we'll delete it to avoid duplicates
        file_list = drive.ListFile({'q': f"title='{file_name}' and trashed=false"}).GetList()
        for file in file_list:
            file.Delete()  # Delete the previous file
        
        # Create & upload new file
        file = drive.CreateFile({'title': file_name})
        file.SetContentFile(file_path)
        file.Upload()
        
        # Create a shareable link (anyone with link can view)
        file.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'
        })
        
        # Get the shareable link
        file_url = file['alternateLink']
        
        # Generate WhatsApp and Telegram links
        whatsapp_link = f"https://wa.me/?text=Check%20out%20this%20loan%20recovery%20report%20{urllib.parse.quote(file_url)}"
        telegram_link = f"https://t.me/share/url?url={urllib.parse.quote(file_url)}&text=Check%20out%20this%20loan%20recovery%20report"
        
        return file_url, whatsapp_link, telegram_link
    except Exception as e:
        st.error(f"Error uploading to Google Drive: {e}")
        # Return fallback values if upload fails
        return "#", "#", "#"

# Function to implement copy functionality with integrated button
def implement_copy_functionality(data):
    # Generate the tabular text
    tabular_text = data.to_csv(sep='\t', index=False)
    
    # Escape any quotes in the text to avoid breaking the JavaScript
    escaped_text = tabular_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
    
    # HTML and JavaScript for the copy button with enhanced styling
    copy_html = f"""
    <style>
        /* Enhanced copy button styling */
        #copy_button {{
            background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
        color: white !important;  /* Ensure text remains visible */
        font-weight: bold;
        border: none;
        padding: 12px 35px;
        border-radius: 12px;
        box-shadow: 0 5px 10px rgba(255, 65, 108, 0.4);
        font-size: 12px;
        transition: all 0.3s ease-in-out;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 1px;
        }}
        
        #copy_button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(255, 65, 108, 0.6);
            background: linear-gradient(135deg, #FF4B2B 0%, #FF416C 100%);
        }}
        
        #copy_button:active {{
            transform: translateY(1px);
            box-shadow: 0 2px 8px rgba(255, 65, 108, 0.5);
        }}
        
        
         #success_message {{
            background-color: #4CAF50;
            color: white;
            padding: 8px 12px;
            border-radius: 12px;
            text-align: center;
            max-width: 200px;
            display: none;
            font-weight: bold;
            font-size: 14px;
            position: fixed;
            bottom: 30px;
            left: 30px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            z-index: 1000;
            animation: slide-in 0.3s ease-out;
        }}
        
        @keyframes slide-in {{
            0% {{ transform: translateX(-100%); opacity: 0; }}
            100% {{ transform: translateX(0); opacity: 1; }}
        }}
        
        @keyframes fade-out {{
            0% {{ opacity: 1; }}
            100% {{ opacity: 0; }}
        }}
    </style>
    
    <button id="copy_button">📋 COPY GENERATED REPORT</button>
    <div id="success_message">✓ Report copied to clipboard!</div>
    
    <script>
        document.getElementById('copy_button').addEventListener('click', function() {{
            const textToCopy = "{escaped_text}";
            
            // Create a temporary textarea element
            const textarea = document.createElement('textarea');
            textarea.value = textToCopy;
            textarea.setAttribute('readonly', '');
            textarea.style.position = 'absolute';
            textarea.style.left = '-9999px';
            document.body.appendChild(textarea);
            
            // Select the text
            textarea.select();
            
            try {{
                // Try to copy using the Clipboard API first (modern browsers)
                navigator.clipboard.writeText(textToCopy)
                    .then(() => {{
                        showSuccess();
                    }})
                    .catch(() => {{
                        // Fall back to execCommand for older browsers
                        document.execCommand('copy');
                        showSuccess();
                    }});
            }} catch (err) {{
                // If both fail, try one more time with execCommand
                document.execCommand('copy');
                showSuccess();
            }}
            
            // Clean up
            document.body.removeChild(textarea);
        }});
        
        function showSuccess() {{
            const successMsg = document.getElementById('success_message');
            successMsg.style.display = 'block';
            setTimeout(function() {{
                successMsg.style.display = 'none';
            }}, 3000);
        }}
    </script>
    """
    
    # Rendering the HTML component with increased height to accommodate the button
    st.components.v1.html(copy_html, height=120)
    
# Streamlit app - Use custom HTML for more vibrant title
st.markdown('<div class="main-title">LoanWise - Smart Loan Recovery System〽️📈</div>', unsafe_allow_html=True)

# Adding Logo, Welcome Message, and Intro Video in the sidebar
logo_path = "LoanWise logo.jpg"
st.sidebar.markdown(
    f"<div style='text-align: center;'><img src='data:image/jpeg;base64,{base64.b64encode(open(logo_path, 'rb').read()).decode()}' width='180'></div>",
    unsafe_allow_html=True
)
st.sidebar.markdown("<h3 style='text-align: center; color: #FFD700; text-shadow: 1px 1px 2px #000000;'>Welcome to Smart Loan Recovery System</h3>", unsafe_allow_html=True)

# Add intro video to the sidebar with autoplay
video_path = "Intro video 4 LoanWise.mp4"
st.sidebar.video(video_path)
st.sidebar.markdown("<div class='content-text'>This system helps financial institutions efficiently manage loan recovery by analyzing risk and suggesting tailored recovery strategies.</div>", unsafe_allow_html=True)

option = st.radio("Choose an option:", ('Single Entry', 'Bulk Upload'))

if option == 'Single Entry':
    # Single entry code remains the same...
    st.markdown('<div class="custom-subheader">Fill Borrower Details</div>', unsafe_allow_html=True)
    
    # Creating a more visually appealing layout with columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Age: 18-75 (realistic borrowing age range)
        age = st.number_input('Age', min_value=18, max_value=75, value=25, step=1)
        # Monthly Income: Min 5000, realistic upper limit 500000
        monthly_income = st.number_input('Monthly Income', min_value=5000.0, max_value=500000.0, value=30000.0, step=1000.0)
        # Loan Amount: Min 10000, realistic upper limit 10000000
        loan_amount = st.number_input('Loan Amount', min_value=10000.0, max_value=10000000.0, value=500000.0, step=10000.0)
        # Loan Tenure: 6 to 360 months (6 months to 30 years)
        loan_tenure = st.number_input('Loan Tenure (months)', min_value=6, max_value=360, value=120, step=6)
        # Interest Rate: 1% to 30% (realistic range)
        interest_rate = st.number_input('Interest Rate (%)', min_value=1.0, max_value=30.0, value=8.5, step=0.1)
    
    with col2:
        # Collateral Value: Optional but shouldn't be negative
        collateral_value = st.number_input('Collateral Value', min_value=0.0, max_value=10000000.0, value=0.0, step=10000.0)
        # Outstanding Loan Amount: Shouldn't exceed loan amount
        outstanding_loan_amount = st.number_input('Outstanding Loan Amount', min_value=0.0, max_value=loan_amount, value=loan_amount * 0.8, step=10000.0)
        # Monthly EMI: Shouldn't exceed monthly income
        monthly_emi = st.number_input('Monthly EMI', min_value=0.0, max_value=monthly_income * 0.8, value=monthly_income * 0.4, step=1000.0)
        # Number of Missed Payments: 0 to 24 (up to 2 years of missed payments)
        num_missed_payments = st.number_input('Number of Missed Payments', min_value=0, max_value=24, value=0, step=1)
        # Days Past Due: 0 to 720 days (up to 2 years overdue)
        days_past_due = st.number_input('Days Past Due', min_value=0, max_value=720, value=0, step=30)

    # Centered button with custom styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button('Predict Recovery Strategy')

    if predict_button:
        input_data = pd.DataFrame([[age, monthly_income, loan_amount, loan_tenure, interest_rate, collateral_value, 
                                   outstanding_loan_amount, monthly_emi, num_missed_payments, days_past_due]],
                                 columns=sample_data.columns[1:])
        risk_score = rf_model.predict_proba(input_data)[:, 1][0]
        
        # More visually striking result display with emojis and better formatting
        st.markdown("<hr style='border: 2px solid white;'>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 24px; font-weight: bold; color: white; text-shadow: 1px 1px 2px black;'>Recovery Strategy Recommendation</div>", unsafe_allow_html=True)
        
        if risk_score > 0.75:
            st.markdown('<div style="background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%); color:white; padding:20px; border-radius:10px; font-size: 20px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.3);animation: pulse 3s infinite;"><span style="font-size: 30px;">⚠️</span><br><b>HIGH RISK</b><br>Immediate legal notices & aggressive recovery attempts</div>', unsafe_allow_html=True)
        elif 0.50 <= risk_score <= 0.75:
            st.markdown('<div style="background: linear-gradient(90deg, #FF8008 0%, #FFC837 100%); color:white; padding:20px; border-radius:10px; font-size: 20px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.3);animation: pulse 3s infinite;"><span style="font-size: 30px;">⚠️</span><br><b>MEDIUM RISK</b><br>Settlement offers & repayment plans</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background: linear-gradient(90deg, #56CCF2 0%, #2F80ED 100%); color:white; padding:20px; border-radius:10px; font-size: 20px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.3);animation: pulse 5s infinite;"><span style="font-size: 30px;">📊</span><br><b>LOW RISK</b><br>Automated reminders & monitoring</div>', unsafe_allow_html=True)

elif option == 'Bulk Upload':
    st.markdown('<div class="custom-subheader">Upload Excel or CSV File</div>', unsafe_allow_html=True)
    
    # Creating a more visually appealing upload area
    st.markdown("""
    <style>
        div.stFileUploader {
            position: relative;
            z-index: 10; /* Brings it above the background */
            top: -12px; /* Adjust positioning */
            background: rgba(255, 255, 255, 0.6); /* Semi-transparent white */
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* Soft shadow for visibility */
        }
    </style>
""", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"],key="uploader")
    st.markdown("<div class='FileUploader'></div>", unsafe_allow_html=True)

    # Download Sample Template - Improved button with same style
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        with open(sample_file_path, "rb") as file:
            st.download_button(
                label="📥 Download Sample Template",
                data=file,
                file_name="sample_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)

            # Check for missing columns
            missing_columns = [col for col in sample_data.columns if col not in data.columns]
            if missing_columns:
                st.markdown(f'<div style="background-color: #FF5252; color: white; padding: 10px; border-radius: 5px;"><b>ERROR:</b> Missing required columns: {missing_columns}</div>', unsafe_allow_html=True)
            elif data.empty:
                st.markdown('<div style="background-color: #FF5252; color: white; padding: 10px; border-radius: 5px;"><b>ERROR:</b> The uploaded file is empty. Please provide valid data.</div>', unsafe_allow_html=True)
            else:
                features = data.drop(columns=['Customer_ID'])
                data['Risk_Score'] = rf_model.predict_proba(features)[:, 1]
                data['Recovery_Strategy'] = data['Risk_Score'].apply(lambda x: "Immediate legal notices & aggressive recovery attempts" if x > 0.75 else \
                                                                  "Settlement offers & repayment plans" if 0.50 <= x <= 0.75 else \
                                                                  "Automated reminders & monitoring")
                
                # Success message with animation
                st.markdown('<div style="background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%); color: white; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.2); animation: pulse 3s infinite;"><span style="font-size: 24px;">✅</span> File Processed Successfully!</div>', unsafe_allow_html=True)
                
                # Add animation keyframes
                st.markdown("""
                <style>
                @keyframes pulse {
                  0% { transform: scale(1); }
                  50% { transform: scale(1.05); }
                  100% { transform: scale(1); }
                }
                </style>
                """, unsafe_allow_html=True)

                # Display data in a table format with colored strategy column
                st.markdown("<div class='custom-subheader'>Results</div>", unsafe_allow_html=True)

                # Creating a function to apply background colors based on the risk level
                def color_risk(val):
                    if val > 0.75:
                        return 'background-color: #FF416C; color: white; font-weight: bold'
                    elif 0.50 <= val <= 0.75:
                        return 'background-color: #FFC837; color: black; font-weight: bold'
                    else:
                        return 'background-color: #56CCF2; color: black; font-weight: bold'

                # Another function to color the strategy column
                def color_strategy(val):
                    if 'Immediate' in val:
                        return 'background-color: #FF416C; color: white; font-weight: bold'
                    elif 'Settlement' in val:
                        return 'background-color: #FFC837; color: black; font-weight: bold'
                    else:
                        return 'background-color: #56CCF2; color: black; font-weight: bold'

                # Applying the styling to the dataframe
                styled_data = data.style.map(color_risk, subset=['Risk_Score']).map(color_strategy, subset=['Recovery_Strategy'])

                # To Display the styled dataframe
                st.dataframe(styled_data)

                # Save processed results
                processed_file_path = 'processed_results.xlsx'
                data.to_excel(processed_file_path, index=False)
                
                # Creating a buffer for the Excel file
                excel_buffer = BytesIO()
                data.to_excel(excel_buffer, index=False)
                excel_buffer.seek(0)
                
                # Upload to Google Drive and get sharing links
                file_url, whatsapp_link, telegram_link = get_shareable_links(processed_file_path, "processed_results.xlsx")
                
                # Add the new copy functionality
                st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                implement_copy_functionality(data)
                
                # Creating sharing options container with improved styling
                st.markdown('<div class="custom-subheader" style="margin-top: 20px;">Share Results</div>', unsafe_allow_html=True)
                st.markdown('<div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 10px;">', unsafe_allow_html=True)
                
                # Creating a container for all buttons with flex layout
                st.markdown('<div class="buttons-container">', unsafe_allow_html=True)
                
                # Download results button with uniform styling
                btn1 = st.download_button(
                    label="📥 Download Results",
                    data=excel_buffer,
                    file_name="processed_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_results",
                    use_container_width=True
                )

                # Direct link to the file on Google Drive
                st.markdown(
                    f'<a href="{file_url}" target="_blank" class="uniform-button download">🔗 View on Google Drive</a>',
                    unsafe_allow_html=True
                )

                # WhatsApp sharing button with uniform styling
                st.markdown(
                    f'<a href="{whatsapp_link}" target="_blank" class="uniform-button whatsapp">📱 Share via WhatsApp</a>',
                    unsafe_allow_html=True
                )
                
                # Telegram sharing button with uniform styling
                st.markdown(
                    f'<a href="{telegram_link}" target="_blank" class="uniform-button telegram">📤 Share via Telegram</a>',
                    unsafe_allow_html=True
                )
                
                # Close the buttons container
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.markdown(f'<div style="background-color: #FF5252; color: white; padding: 15px; border-radius: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"><b>ERROR:</b> {e}</div>', unsafe_allow_html=True)

# Footer with copyright
st.markdown('<hr style="margin-top: 30px; border: 1px solid rgba(255,255,255,0.2);">', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align: center; color: rgba(255,255,255,0.7); padding: 10px; font-size: 14px;">'
    '© 2025 LoanWise. All Rights Reserved.<br>'
    '</div>',
    unsafe_allow_html=True
)