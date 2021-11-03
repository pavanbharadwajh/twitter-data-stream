## Twitter Data Stream
Stream Twitter Data into BigQuery, using Pub/Sub.
</br>
![alt text](design.jpg?raw=true)
</br>

The project demonstartes, developement of ETL pipeline on GCP.
- EXTRACT - Connect to the Twitter streaming API and stream raw data into PUB/SUB topic.
- TRANSFORM - Subscribe and pull data from the topic. Filter Data based on Keywords. 
- LOAD - Parse required fields from invidual tweets and send it to Big Query Table.

#### Requirements for the task are:

1. Twitter Developer account
2. Google Cloud Platform account

#### Main steps of process are:

1. Obtaining Twitter credentials
2. Create IAM Service accound and assigned following roles.
    - BigQuery Data Editor
    - BigQuery Job User
    - Dataflow Developer
    - Pub/Sub Editor
3. Create Big-Query table.

#### Run Instructions
1. Clone this repo: `$ git clone https://github.com/pavanbharadwajh/twitter-data-stream.git`
2. Switch into the working directory: `$ cd twitter-data-stream`
3. Create a virtual environment for the python packages: `$ virtualenv venv`
4. Install the project's python dependencies: `pip install -r requirements.txt`
5. Set the values obtained from the previous step in the `.env` file.
6. Run publisher via `python twitter/publisher.py`
7. Run subscriber via `python twitter/subscriber.py`
8. Run Queries via `python twitter/queries.py`

#### Results
The results are stored in the `result` folder. I have also provided the sample data in csv format.

#### Creating a Publisher
PUBLISHER - Listen to streaming Twitter data, I have used tweepy library that takes a list of keywords and filter the real-time tweet stream. Upon receiving the data, the data is published to `tweets` topic of the Pub/Sub model.

#### Creating a Subscriber
SUBSCRIBER - Subscriber pulls the data from Pub/Sub topic `tweets`. The data is filtered based on the keywords and hashtags in tweets related to music. The filtered data is transformed to extract required fields and pushed to Big Query for storage.

A Big Query table is created with the below schema.
- id :	STRING	
- created_at	DATETIME		
- tweet_location	STRING		
- text	STRING		
- retweet_count	INTEGER		
- favorite_count	INTEGER		
- user_name	STRING		
- user_location	STRING		
- user_followers_count	INTEGER		

id is a REQUIRED field and serves as the Primary Key avoiding duplicates.

#### The collected data has the below USECASES:
 1. Determine total tweets about Justin Beiber, for each hour, day, week etc related to music.
 2. Determine region wise tweets count.
 3. Determine social media engagement about Justin Beiber's music during specific times to determine album release date, location etc.
 4. Perform sentimental analysis on the text columns. 

 #### Future Work
 1. Dockerize the application and run it from GCP for end-to-end execution of ETL pipeline on GCP.
 2. Connect the big query table to sophisticated visulization tools, to perform real-time visualizations on the streaming data.

 #### Questions
 1. What are the risks involved in building such a pipeline?
     - Cost: Continued integration with Twitter API (if premium is used) can end up costing money, also will result in added costs during troubleshooting.
     - Consistency: In a streaming job, such as this the data remaining consistent is crucial. Hence we need to be careful while adding new properties or changing them.
     - Availability: All reads to twitter might contain data, but they need not be the most recent. Also, we need to account for changing data. Ex: Missing fields and such.
     - Partition Tolerance: The pipeline continues to operate despite failures of other components.

 2. How would you roll out the pipeline going from proof-of-concept to a production-ready solution?
 From the above architecture diagram, it can be noted that there are 2 major components. A Publisher and a Subscriber. The project can be set in 4 phases. 
     - Phase 1: Publisher, from the POC the purpose of the publisher is clear, which is to ingest stream messages. Few things to consider while developing this is, fault-tolerant and scalability.
     - Phase 2: Resources, PUB/SUB is the major resource here. It is used for data ingestion. Deployment with Optimal configurations for our use case needs to be done. Also, intorducing message schema will grealty benefit.
     - Phase 3: Subscriber, Once the data is ready and can be ingested, an application which can process such large volume of data will be developed. I will choose GCP DATA FLOW in production, as it supports both batch and streaming integrates easily with PUB/SUB providing fully managed streaming analytics service. Also, during phase, we need to deploy the Big Query or DataBase as well for storage.
     - Phase 4: Deployment and Maintainance. Once each of the individual component is up and ready, the deployment startegy of the whole pipeline needs to be finalised in-order to support updating of individual components. (Each of the components are decoupled for this purpose, however needs to tested/finalised as a whole). Maintainance The common issues, troubleshooting steps, and recovery mechanism needs to well documented.

 3. What would a production-ready solution entail that a POC wouldn't?
 As it is a POC, GCP was chosen for ease of use. On rolling out to production the choice of cloud provider may vary based on preference. Following are major changes.
      - PUB/SUB - Its used for data ingestion, and I have deployed it with default options.These options can be tweaked to optimise it based on the production traffic.
            - Flow Contorl: This can help tackle spike in traffic on publisher traffic, instead of dynamicallly autoscaling subscriber resources to consume more messages.
            - Batching: A batch in this context is a group of messages published to a topic.  
            Based on the traffic rate and buisiness use case, batching can also be an option to acheive same throughput with fewer publishes.
      - Decoupling: Currently, the application has both producer and subscriber, decoupling them will make the application more robust and simplify deployment.
            - Publisher and Subscriber can be easily dockerized and deployed.
      - Alerting: Alerting is very crucial, in such an application involving multiple components. Right mechanism  simplifies the troubleshoooting and making it more maintainable.
      - Message Schemas: The data is more than bytes, hence having a schema can solve multiple problems ranging from parsing errors to faster data serialization.
      - Subscriber: Curretly, subscriber is performs a simple keyword search to filter tweets on music. On prod. depending on the traffic, I would deploy a data flow job, which can handle large volume processing.

NOTE: 1 sprint = 15 days/2 weeks

 4. What is the level of effort required to deliver each phase of the solution?
     - Phase 1 - This is the initial phase, and can be delivered within a single sprint.
     - Phase 2 - Although this involves less development (coding), the POC for optimizing might take some time. However, can be delivered in less than a single sprint.
     - Phase 3 - This involves 2 major tasks, of deploying the data storage,and development of robust application to process large dataset. This requires over a sprint.
     - Phase 4 - This is the final step, although involves less coding and more documenting, it ties up all the loose ends and integrates the components as a whole pipeline. This can be delivered in a single sprint.

 5. What is your estimated timeline for delivery for a production-ready solution?
     - The project can be delivered in 4-5 sprints. This can vary based on details unkown from the initial problem statement. Monitoring, Buisiness use case, and other optimization work not a part of this POC.
