import streamlit as st

from forms.contact import contact_form

@st.dialog('Contact Me')
def toggle_contact_form():
    contact_form()

col1, col2 = st.columns(2, gap='medium', vertical_alignment='bottom')
with col1:
    st.image(r'./assets/IMG_1898-EDIT-EDIT.jpg', use_container_width=True, caption='Grand Canyon, South Rim, April 2024',clamp=False)

with col2:
    st.title('Ian Temchin', anchor=False)
    st.caption('B.S. Environmental Science')
    st.write(
        'Skilled environmental scientist and data analyst, bridging the gap from idea to insight, and delivering informed solutions in any context.'
    )

    cola, colb = st.columns(2, gap='small')
    with cola:
        if st.button('✉️ Contact Me'):
            toggle_contact_form()


    with colb: 
        st.link_button('Linkedin', r'https://www.linkedin.com/in/iantemchin/')

       
# --- EXPERIENCE & QUALIFICATIONS ---
st.write('\n')
env, data =st.tabs(['Environmental Remediation', 'Data Analysis'])
with env:
    st.subheader('Experience')
    st.markdown('''- A decade of experience planning and implementing investigation and remediation of contaminated sites. Strong foundations in field work with excellent project management and data analysis skills.        
- Five years experience managing complex munitions response sites in remote locations contaminated with high-explosives and chemical warfare materiel.                
- Specialize in management and analysis of environmental data including field data and analytical chemistry reports.
- Proven leader, driven by data to empower teams delivering successful project outcomes and improved operations.
''')
    
    st.subheader('Technical Skills & Competencies')
    st.write('''
             - Project Management
             - Stakeholder Collaboration and Engagement
             - Site Management, Contractor Oversight, Team Leadership
             - Environmental Sample Collection
             - Environmental, Geophysical, and Geotechnical Data Collection
             - Data Visualization, Modeling, and Statistical Analysis
             - NJ CSSR (N.J.A.C 7:26C-E), CERCLA, DERP-FUDS MMRP
             ''')

    
    st.subheader('Certifications')
    st.write('''
        - OSHA 40-Hour HAZWOPER
        - OSHA 8-Hour Confined Space Entry Training
             ____
    ''')    

    with open(r'./assets/Resume_2025_Temchin.docx.pdf','rb') as resume:
        pdfbyte = resume.read()
        st.download_button(
            label='📃 Remediation Resume (pdf)', data=pdfbyte, file_name='Temchin Resume, env remediation.pdf',mime='application/octet-stream')

    with open(r'./assets/Copy of OSHA_40-hour_2011-2012.pdf', 'rb') as hazwoper:
        pdfbyte = hazwoper.read()
        st.download_button(
            label='🪪 40HR HAZWOPER (pdf)', data=pdfbyte, file_name='Temchin HAZWOPER40.pdf',mime='application/octet-stream')

with data:
    st.subheader('Experience')
    st.markdown('''- A decade of practical experience managing, analyzing, and reporting on large environmental data sets.                
- Three years experience as the general manager of a b2b agricultural wholesale production facilty, providing operational, production, and wholesale business analytics directly to the C-Suite.                
- Demonstrated expertise in statistical principles applied to sampling design and data analysis.                
- Proven leader, driven by data to empower teams delivering successful project outcomes and improved operations without compromising safety, quality, efficiency, or regulatory compliance.
''')
    
    
    st.subheader('Technical Skills')
    st.write('''
             - Programming: Python, Google Apps Script, VBA
             - Data Analysis: SQL, pandas, Earthsoft EQuIS
             - Data Visualization: Matplotlib, seaborn, MS Excel, ESRI ArcMap
             - Modeling and Statistical Analysis
''')
    st.subheader('Certifications')
    st.link_button('Data Analysis with Python', r'https://freecodecamp.org/certification/fcc124191a0-541b-44ec-b544-de09a6c76253/data-analysis-with-python-v7')
    

        