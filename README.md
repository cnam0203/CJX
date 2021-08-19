![logo](https://user-images.githubusercontent.com/47789251/129663401-e1c28faf-a96f-49f6-a146-497c912df041.gif)

# Customer Journey Master
Customer Journey Master is a Web Management Application written by Python's Django web framework, targeting small and medium businesses, assisting them in collecting and managing customer journey data from multiple sources and channels in one place, analyzing and exploiting the journey based on Process Mining and Machine Learning techniques.

## Main Functions
  1. Create data sources (dataset) for analyzing customer journey data
  2. Import customer journey data into data sources by uploading CSV Files (limit 15 MB for each upload file)
  3. Import customer journey data into data sources by pre-defined RestfulAPI endpoint
  4. Visualize the entire customer journey based on Process Mining Algorithms, including: Alpha Miner, Heuristic Miner and Inductive Miner
  5. Cluster customer journeys into similar groups based on Clustering Algorithms, including: KMeans and KModes
  6. Find decision points that influence customers' choices through the entire process based on Decision Tree Algorithm
  7. Store analytical results and review
  8. View daily metrics reports by charts 

## Installation
  ### Environment requirements:
   1. Python
   
        - Django is a Python web framework, so, we have to download python on the machine, so that we can run the server. We recommend downloading Python version from 3.x.x .
        <img width="798" alt="Screen Shot 2021-08-19 at 12 35 10" src="https://user-images.githubusercontent.com/47789251/130013579-00b9af10-1f52-4dc8-95fc-2aed8973b9e1.png">

   2. Database (MySQL)
    
        - The system needs a database management system to store customer data, so it needs to install a DBMS. The source code of this system, currently supports MySQL, so we recommend you to install MySQL. However, you can still load other DBMS systems (PostgreSQL, SQL Server, ...), and then need to reconfigure the database engine in the project's settings.py file, to enable the connection between backend server and database server.

        <img width="888" alt="Screen Shot 2021-08-19 at 12 36 23" src="https://user-images.githubusercontent.com/47789251/130013674-e44eac99-002b-4ce9-9054-c661f8572960.png">
        
        - Once installed, you need to create a database, name it and save the database account information: hostname, port, username, password and database name.
    
   3. Pip
   
        - A package manager for Python.
        
        <img width="843" alt="Screen Shot 2021-08-19 at 12 37 11" src="https://user-images.githubusercontent.com/47789251/130013761-0d44f686-68ce-4256-abaf-6820e5e0bc9e.png">

   4. Virtual environment 
      
        - A tool to create isolated Python environments. A Python environment such that the interpreter, packages, libraries, and scripts installed into it are isolated from those installed in the global environment of the system. It also allows installing packages without administrator privileges. Django package, the process mining library will be stored in the directory of the virtual environment.

      <img width="895" alt="Screen Shot 2021-08-19 at 12 37 42" src="https://user-images.githubusercontent.com/47789251/130013803-f3c2ccd9-9f66-45d9-bd08-d21e5ec944fb.png">

      
  ### Main steps
   1. Clone source code
      - Create an empty folder for project
      
        <img width="634" alt="Screen Shot 2021-08-17 at 13 44 43" src="https://user-images.githubusercontent.com/47789251/129676791-25087a67-3d23-49fe-83fe-a5f92f07f3a3.png">
        
      - Clone source code into created folder, following the link:
        https://github.com/cnam0203/CJX.git
       
   
   2. Virtual environment
   
      - Create a virtual environment folder in the root of folder:
      
        <img width="695" alt="Screen Shot 2021-08-17 at 13 55 53" src="https://user-images.githubusercontent.com/47789251/129678303-e2fb43f5-89af-41e3-8895-adf3305a3e4b.png">
        
      - Activate virtual environment and then installing Python packages for project:
      
        <img width="691" alt="Screen Shot 2021-08-17 at 13 56 54" src="https://user-images.githubusercontent.com/47789251/129678433-5b414ef7-99d1-4caf-bb02-46ec23ed78a0.png">
      
        <img width="866" alt="Screen Shot 2021-08-17 at 13 59 00" src="https://user-images.githubusercontent.com/47789251/129678743-e2f49878-6bb2-477f-8b9d-14eaecaf6c06.png">
   
   3. Configuration

      - First, Go the the cjx_project folder.
      - Configure information relating to database server, in 'cjx_project/settings.py' file:
      
        <img width="384" alt="Screen Shot 2021-08-19 at 13 05 22" src="https://user-images.githubusercontent.com/47789251/130016448-a710145c-1d23-410c-987a-a3154a423a78.png">


      
      - Migrate pre-defined tables (admin, permission, session, etc.) into database
      
        <img width="824" alt="Screen Shot 2021-08-17 at 14 07 10" src="https://user-images.githubusercontent.com/47789251/129679826-743919cf-b1e9-4557-972c-8ef4918f3a84.png">
   
   4. Start server

      - Now, we can run starting system

        <img width="847" alt="Screen Shot 2021-08-17 at 14 07 59" src="https://user-images.githubusercontent.com/47789251/129679942-9a723e01-b219-40b1-b6e8-3c255ee1c91f.png">
        
      - By default, the server run on port 8000, we can change the port with the following command
      
        <img width="874" alt="Screen Shot 2021-08-17 at 14 10 26" src="https://user-images.githubusercontent.com/47789251/129680264-e65a2db2-cd09-4848-8dc1-cf5581d4e90e.png">

      - Go to the link: http://127.0.0.1:8000/ to check whether server runs. If OK, it will display an Authentication screen

        <img width="1440" alt="Screen Shot 2021-08-17 at 14 11 55" src="https://user-images.githubusercontent.com/47789251/129680430-79821d66-7606-4b60-bea8-dd72437f2e7b.png">


      
  
## How to use
  ### Data Model
   In order to run analysis in system, it requires that customer journey we import must have a pre-defined format. Each customer data is an event/an interraction between customer and company that can be tracked. Neccessary fields for an interraction are described in below table:
   
   | Fieldname | Describe |
   | --------- | -------- |
   | Customer ID | unique ID for each customer |
   | Action type | customer activity (ask for information, technical support, view product info, view product list, ...) |
   | Time | moment when customer executed the touchpoint |
   | Channel type | where customer executed the touchpoint (website, mobile app, call center, offline store) |
   | Device category | name of device category (smartphone, tablet, laptop,...) |
   | Device OS | name of operating system (Windows, MacOS, Ubuntu,...) |
   | Device Browser | name of browser (chrome, safari, edge,...) |
   | Geo-country | geo-network data about country tracked from device when customer executed the touchpoint |
   | Geo-city | geo-network data about city tracked from device when customer executed the touchpoint |
   | Traffic source | which source triggers customer touchpoint |
   | Store | physical store name where the customer directly interacts with the service of the company |
   | Employee | employee name where the customer directly interacts with the service of the company |
   | Webpage hostname | hostname of website which customer executed the touchpoint |
   | Webpage url | URL of website which customer executed the touchpoint |
   | Webpage title | title of page on website which customer executed the touchpoint |
   | App name | mobile app name that customer executed the touchpoint |
   | App screen title | title of screen on mobile app that customer executed the touchpoint |
   | Interract item type | name of interact item (product, transaction, video, ...) |
   | Interract item url | URL of item that customer interacted through the touchpoint (video_url, ...) |
   | Interract item content | content of item that customer interacted through the touchpoint (email content, ...) |
   | Experience emotion | name of experience emotion (happy, angry, satisfied, ...) |
   | Experience score | score that customer evaluated for the touchpoint experience |
  
  A customer data does not need to have all the fields listed above. However, required fields include: customer_id, time and action_type. The remaining fields can be used to analyze customer bahavior or customer habits.
    
  ### Admin
  Admin is the first account that needs to be created after installing the system. Admin can create staff accounts (analyst, company's marketer).
Besides, the admin also has the right to create data sources (datasets) containing customer data. In addition, the admin can authorize staff accounts or other systems to import data into these data sources or run analysis based on these imported data.

   1. Create admin account
   
      - Run the following command and enter information account
   
          <img width="891" alt="Screen Shot 2021-08-17 at 14 51 11" src="https://user-images.githubusercontent.com/47789251/129686123-7f6811a1-acf0-4f31-8a9b-395d8560f1a3.png">
  
      - Check admin account is created, browse the link: http://127.0.0.1:8000/admin
   
          <img width="959" alt="Screen Shot 2021-08-17 at 14 52 23" src="https://user-images.githubusercontent.com/47789251/129686272-e75b4af6-3193-4c8d-baed-077ec1952c63.png">
      
      - Enter account just created. Then we can go to the admin site:
   
          <img width="686" alt="Screen Shot 2021-08-17 at 14 53 45" src="https://user-images.githubusercontent.com/47789251/129686467-7bea1d36-d83b-4c79-a743-0e9e4e9e6424.png">

   2. Add staff account

      - Create staff accounts, enable them to connect to analysis website
   
          <img width="1417" alt="Screen Shot 2021-08-17 at 14 55 14" src="https://user-images.githubusercontent.com/47789251/129686699-e05fdfad-c6aa-41c0-ba62-25561d3c5ac0.png">
  
   3. Create data source
   
      - A data source is the storage that we can import customer data into. Admin can create multiple data sources and set data source private or public. If data source is public, all staff accounts can see data.

          <img width="1405" alt="Screen Shot 2021-08-17 at 14 57 30" src="https://user-images.githubusercontent.com/47789251/129687060-af4b23d6-009e-4223-8989-0345c08935b2.png">

   4. Grant permission for data source
   
      - If a data source is set public, all staff accounts can see all customer data in it. However, to enable staff accounts perform analysis functions with the data source, admin need to grant permission for staff account.

          <img width="1098" alt="Screen Shot 2021-08-17 at 14 59 40" src="https://user-images.githubusercontent.com/47789251/129687399-8b97363d-42ed-4bd6-9fc5-648a6dd88d67.png">

   5. Create API Token

      - To enable other systems import tracking customer data into data source, admin can create an API token and send it to other systems. When the others systems post customer data into data source through Restful API endpoint, they need to add API token in request header.

          <img width="801" alt="Screen Shot 2021-08-17 at 15 02 58" src="https://user-images.githubusercontent.com/47789251/129687886-bb07e28e-0ae0-48a8-bf2a-b7b5b3921cef.png">

  ### Staff
   1. Create data source

      - Just like admin accounts, staff accounts can also create data sources. However, these data sources are private, which means that only staff creates that data source and runs analysis on that data source.
   
   2. Create matching file
   
      - After creating the data source, the staff account can import customer data into the data source. Create mapping file is a function that allows the user to create a file, this file has the function of matching the data structure of the data in the csv file with the data structure of the table in the database. Staff can reuse this matching file multiple times.

        <img width="588" alt="Screen Shot 2021-08-17 at 15 10 17" src="https://user-images.githubusercontent.com/47789251/129688927-1b200a09-6dba-4f26-9510-c3c4e4028812.png">

        <img width="667" alt="Screen Shot 2021-08-17 at 15 10 40" src="https://user-images.githubusercontent.com/47789251/129688974-359b26e6-0da5-40f0-ad9f-c2535293a907.png">

   
   3. Upload CSV File

        - Then, the staff can upload data to the system through the customer data contained in the csv file.
        - Staff match data structure and choose data source.

            <img width="981" alt="Screen Shot 2021-08-17 at 15 12 47" src="https://user-images.githubusercontent.com/47789251/129689254-71b78c61-512d-4a76-8145-d5501a28742f.png">

   
   4. Remove data

         - All data that staff import into the system is logged. Staff can review log history and delete imported data based on stored information.

            <img width="943" alt="Screen Shot 2021-08-17 at 15 15 48" src="https://user-images.githubusercontent.com/47789251/129689775-bbde04e9-4d88-4c49-9e72-30e6e415a7f7.png">


   5. Visualize Process Graph
   
         - Visualize process graph is an analysis function that helps convert customer journey data into a process graph based on 3 main process discovery algorithms: Alpha miner, Heuristic miner and Inductive miner. The process graph is capable of depicting the entire customer journey. Staff can choose algorithm, time of customer journey data and data source.

            <img width="879" alt="Screen Shot 2021-08-17 at 15 20 20" src="https://user-images.githubusercontent.com/47789251/129690481-395831a0-ef34-4856-882c-28e735782caf.png">
            
            <img width="873" alt="Screen Shot 2021-08-17 at 15 21 20" src="https://user-images.githubusercontent.com/47789251/129690631-cc2debb2-31a4-461d-84d1-41455c90b804.png">


   6. Trace Clustering
      
         - Trace clustering is the function of clustering similar customer journeys into groups. It allows to simplify the process graph generated from the "Visualize process graph" step above. Staff can know which of the most common customer journeys are taking place, thereby recommending appropriate business strategies. 
         - We allow staff to choose from two clustering algorithms: K-Means and K-Modes and two preprocessing methods: Bag-of-activities and Sequence-vector.

   7. Decision Mining

        - Decision mining is a function that helps staff find decision points that influence customer choices in their journey. These decision points can be customer habits like: device, channel, etc. We use this decision tree algorithm to find the decision points.

            <img width="670" alt="Screen Shot 2021-08-17 at 15 29 25" src="https://user-images.githubusercontent.com/47789251/129691813-67f7d5a0-2649-4a86-8446-c2c9263139ea.png">

   
   8. Review analytical history

        - All results, algorithms, data sources, and time taken by staff to run the analysis are saved in the database.

            <img width="987" alt="Screen Shot 2021-08-17 at 15 32 21" src="https://user-images.githubusercontent.com/47789251/129692235-24401169-90e9-4ad9-b089-d015e7dd1f39.png">

   9. View daily metrics report

        - Staff can view charts of customer volume, daily customer interaction based on attributes like device, action, channel from data sources.

          <img width="962" alt="Screen Shot 2021-08-17 at 15 36 00" src="https://user-images.githubusercontent.com/47789251/129692775-99b6b734-1f2d-4d40-8ec9-1b1fdb9f01db.png">

   
   10. Read guideline

        - For new staffs, they can read system guideline and follow instructions to step-by-step perform functions.

            <img width="945" alt="Screen Shot 2021-08-17 at 15 34 07" src="https://user-images.githubusercontent.com/47789251/129692498-f55fca69-865a-440b-a899-ff1194cbd920.png">

  ### Other system
   1. Import data by Restful API endpoint
      
        - To help automatically import customer journey data into data sources, the system allows customer systems to send tracking customer journey data through Restful API endpoints. These requests require an API Token that the admin has created, to enter the request "header", the request "method" is "POST", and the data needs to be in the format of customer data as in the table above, put in in the request "body".
        
            <img width="934" alt="Screen Shot 2021-08-17 at 15 42 43" src="https://user-images.githubusercontent.com/47789251/129693800-63ec5620-0271-4f39-aada-54e9111626c3.png">
        
            <img width="631" alt="Screen Shot 2021-08-17 at 15 43 00" src="https://user-images.githubusercontent.com/47789251/129693854-5cccb789-65c3-4c43-a8a2-207c22bec7bc.png">


        - Response results include status code and message.\
            Successful request:\
                  <img width="383" alt="Screen Shot 2021-08-17 at 15 43 14" src="https://user-images.githubusercontent.com/47789251/129693963-016cb575-5075-4806-8ec7-fdfdd9ed1944.png">
                  
            Failed request with no auth:\
                  <img width="312" alt="Screen Shot 2021-08-17 at 15 43 59" src="https://user-images.githubusercontent.com/47789251/129694000-01ef5a33-bd96-4b6f-a611-dc3ec3b10d9c.png">
            
            Failed request with invalid API token:\
                  <img width="310" alt="Screen Shot 2021-08-17 at 15 44 37" src="https://user-images.githubusercontent.com/47789251/129694103-af520c95-c9a3-4142-9999-330830b10c6d.png">
            
            Failed request with invalid API token:\
                  <img width="322" alt="Screen Shot 2021-08-17 at 15 44 59" src="https://user-images.githubusercontent.com/47789251/129694165-3dc33c2a-9378-4f23-b6c9-33b6d67d3c10.png">

  
 ## How to deploy system on cloud services
   1. Amazon Web Service
   
   2. Configuration
      - Project
      - Gunicorn
      - Nginx

  
    
    
