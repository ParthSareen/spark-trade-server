import streamlit as st

st.set_page_config(page_title="Our Blog", page_icon="📝")

st.markdown("""
    # Blog Post 10
    #### March 18th, 2024
    
    ### Mechanical Updates:
    Working on finishing the CAD
    The CAD will be updated along with the electrical improvements and the final enclosure will be fabricated on CNC.
            """)
st.image("./blog_images/week 10.png")
st.markdown("""
    ### Electrical Updates:
    Detail on subtopic 1.

    ### Software Updates:
    The AI model has now been successfully trained and has yielded solid results. This model will be run on the cloud, on our EC2 instance to have minimal strain on the users
    devices, and on the limited hardware in the smart meter. Integration work will be our primairy focus from here on out, as all of the individual components are now complete.
    Currently, we have several mock interfaces up and running to visualize the website, and as we continue our integration work, each mock component will be replaced with the actual data.
    
    """, unsafe_allow_html=True)

st.markdown("""
    # Blog Post 9
    #### March 11th, 2024
    
    ### Mechanical Updates:
    3D printed the second prototype
""")
st.image("./blog_images/week 9.png")
st.image("./blog_images/week 9 again.png")
st.markdown("""        
    ### Electrical Updates:
    Detail on subtopic 1.

    ### Software Updates:
    We have completed the buyer interface, which now completes the loop and lets users both place buy and sell bids. These bids are automatically matched through our algorithm,
    and the buyer is notified once they have successfuly purchased energy. We have also started work on the AI model, as it is currently being trained on the open data provided
    by the government of Ontario. Our hopes are that once it is successfuly trained, it would be able to forecast the price of energy directly, and display that to the user.
    
    """, unsafe_allow_html=True)

st.markdown("""
    # Blog Post 8
    #### March 4th, 2024
    
    ### Electrical Updates:
    Detail on subtopic 1.

    ### Software Updates:
    Now we have created a direct way for the users to interface with the market, allowing users to set up selling bids, which is then fed back into the market grid and is
    able to be matched accordingly. Sellers are able to submit their bids for matching, which then attempts to match them with a buy bid currently present on the market.
    If this fails, the sellers bid still remains on the market until it finds a buyer.
    
    """, unsafe_allow_html=True)

st.markdown("""
    # Blog Post 7
    #### February 26th, 2024
    
    ### Mechanical Updates:
    Pieces to build up the diorama were ordered. These included items such as houses, roads, traffic signs, and grass.
""")
st.image("./blog_images/week 7.png")
st.markdown("""
    ### Electrical Updates:
    Detail on subtopic 1.

    ### Software Updates:
    We've now setup a mock trading interface, and we're able to simulate real time trades between multiple users, with both buyers and sellers present. The market grid has 
    bids for both buying and selling, and they all interact as expected.
    
    """, unsafe_allow_html=True)

st.markdown("""
    # Blog Post 6
    #### February 19th, 2024
    
    ### Electrical Updates:
    Detail on subtopic 1.

    ### Software Updates:
    On our platform, we've rolled out a feature that allows users to create and submit bids directly to the energy market.

    With this update, participants can now easily offer or request energy through our platform. The system is designed around two main components: Actors and Bids. Actors represent
    users within the system, each with their unique attributes, such as type (producer or consumer) and capacity. Bids, on the other hand, detail the offer or request, specifying the
    amount of energy and the price.

    This feature also includes safeguards and mechanisms for managing bids, such as removing outdated offers and matching bids based on criteria like price and quantity. With these 
    capabilities, our platform aims to foster a lively and competitive marketplace, encouraging users to engage in energy trading.

    """, unsafe_allow_html=True)

st.markdown("""
    # Blog Post 5
    #### February 12th, 2024
    
    ### Electrical Updates:
    Detail on subtopic 1.

    ### Software Updates:
    We've recently rolled out the Energy Market page on our platform, a straightforward addition aimed at simplifying how users view and engage with energy trades. 
    This new page features a live Grid View that displays current energy transactions, with sellers highlighted in green and buyers in orange, making it easy to 
    understand market dynamics at a glance. Users can now submit their energy sell bids through this page, with a progress bar guiding them through the submission process
    and a confirmation message to signal successful entry into the market. This page streamlines the process of participating in the energy market, all while keeping interactions secure and data up-to-date through our Flask API.
    As we gear up for our upcoming symposium, the Energy Market page stands ready to demonstrate its value, showcasing live energy trading in a simple and effective manner.
    
    """, unsafe_allow_html=True)

st.markdown("""
    # Blog Post 4
    #### February 5th, 2024
    
    ### Mechanical Updates:
    Printed various options to decide the desired casing 
""")
st.image("./blog_images/week 4.png")
st.image("./blog_images/week 4 again.png")
st.markdown("""
    ### Electrical Updates:
    Detail on subtopic 1.

    ### Software Updates:
    In our latest sprint, we've introduced the metrics page. 
    This week, our team focused on the Metrics Page for each user. This feature directly interfaces with the smart meter devices to fetch real-time data, providing users with 
    an in-depth look at their current energy consumption, including statistics like amps and voltage. This direct data pull from the devices ensures accuracy and timeliness 
    of the information, making it a reliable source for monitoring energy usage.
            
    A key highlight of the Metrics Page is the dynamic graph showing the state of charge over time. This graphical representation is allows users to visually comprehend their
    energy consumption patterns and the efficiency of their energy use. By observing the trends in their energy state of charge, users can identify areas for optimization, 
    potentially leading to savings and more sustainable energy consumption habits. Again, streamlit has made this incredibly easy through the user of Altair charts.

    The backend implementation of the Metrics Page involves our Flask API, which acts as the bridge between the smart meters and our Streamlit application. Utilizing our API calls, 
    authenticated through our saved users and API key. The seamless integration with a Python-based charting library allows for an interactive and engaging presentation of the energy 
    data, enhancing the overall user experience on our platform, and will be key in our symposium demo.

    """, unsafe_allow_html=True)

st.markdown("""
    # Blog Post 3
    #### January 29th, 2024
    
    ### Electrical Updates:
    Detail on subtopic 1.

    ### Software Updates:
    Our flask API is now up and running on a deployed instance! This is our bread and butter from here on out, and the client side streamlit will only be used for basic logic, rendering,
    and making API calls. We have basic level authentication implemented for our API calls, where each call needs an API key to be authorized to prevent someone from randomly scraping this
    endpoint and flooding our EC2 instance with calls, charging us who knows how much in usage and probably bringing down the micro instance we have running. Our current flow is the following;
    
            Streamlit app <-> API <-> Smart meter
    
    Our smart meter will communicate with our streamlit application using the API, and vice versa. All of our data will be running through that, and all information coming from the API will be
    considered a source of truth.
    
    """, unsafe_allow_html=True)

st.markdown("""
    # Blog Post 2
    #### January 22nd, 2024

    ### Electrical Updates:
    Detail on subtopic 1.

    ### Software Updates:
    Started grinding out implementation. Our main pages that we want are the Dashboard, Energy Market view, a login page, a metrics page, and an interactive demo, a live buyer view.
    At this point, a login flow has been implemented. We've also decided to omit using a database for Symposium purposes - as more moving parts have a higher likelihood to break, and migration
    to using a database from local storage is quite easy. For the purposes of the demo, it makes more sense to avoid playing with Redis on a production server. The login flow is quite simple,
    and account creation is supported, and we have cookies to track the user session to maintain the correct data flow for each user.
    
    """, unsafe_allow_html=True)

st.markdown("""
    # Blog Post 1
    #### January 15th, 2024
    
    Back from winter break!
    
    ### Mechanical Updates:
""")
st.image("./blog_images/week 1.png")
st.markdown("""
    Finalized the requirements of the symposium day:

    * 1 Main House (With the smart meter)
        * Smart Meter
        * Consumer (Motor + LED)
        * Producer (Battery Bank with a fake solar panel)
        * Battery storage (also a battery bank)
    * 1st Secondary House
        * Producer (Another battery bank)
        * Consumer (LED + Motor)
    * 2nd Secondary House
        * Consumer (LED + Motor)
            
    ### Electrical Updates:
    Detail on subtopic 1.

    ### Software Updates:
    More planning! Now that we have our architecture chosen and planned, its time to decide on a tech stack and how we're actually going to go about implementing it.
    Our main options are the following:
    * MERN stack application - use React, Node, Redis, and Express.
        * Might be a bit overkill given our use case, and can be a nightmare to work with with Node dependencies killing eachother
    * Full python application - use Flask, Streamlit, and Redis
        * The simpler / easier approach, would allow for rapid prototyping and development.
    
    We've decided to go ahead with the python application because we love Flask and its simplicity. A great saying in software development is KISS; keep it simple, stupid.
    We have no need for the additional complexities that building a MERN stack application brings, and deployment would be much easier and cleaner if we can avoid spinning up docker containers.
    Going with the python approach makes this project incredibly easily to deploy using AWS EC2, and thats what we will be using moving forward.
                
    """, unsafe_allow_html=True)