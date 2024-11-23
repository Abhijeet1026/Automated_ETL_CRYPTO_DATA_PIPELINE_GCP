# Data Engineering:Automated Crypto Data Pipeline GCP
1. [Introduction](#introduction)
2. [Objective](#objective)
3. [Architectural Solution](#architectural-solution)
4. [Data Pipeline](#Data-Pipeline)
   - Data Extraction
   - Transformations
   - Batch data load
   - Automation
5. [Visualization](#Visualization) 
6. [Summary](#Summary)
7. [Reference](#reference)

# Introduction
The Automated Crypto Data Pipeline and Analytics project focuses on building a robust data pipeline using Google Cloud Platform (GCP) tools to extract, process, and analyze cryptocurrency data from the [CoinGecko](https://docs.coingecko.com/reference/coins-markets) API. CoinGecko, a widely used platform, provides real-time information on various cryptocurrencies, capturing key metrics such as prices, market capitalization, trading volumes, and supply data.

At the heart of this project is a fully automated data pipeline that seamlessly ingests high-frequency crypto data in near real-time. Using GCP tools like Cloud Storage, Cloud Composer, Dataproc, and BigQuery, the pipeline performs efficient data extraction, transformation, and loading (ETL). This setup ensures scalability and reliability, handling large volumes of cryptocurrency data without performance bottlenecks.

The pipeline not only processes raw data but transforms it into meaningful insights, such as identifying the current prices, total supply, trading volumes, and market capitalizations of top-performing coins. This comprehensive approach enables users to understand cryptocurrency trends and make data-driven decisions in an ever-changing market.

By combining the power of the CoinGecko API with the scalability of GCP's data tools, this project demonstrates how cloud-based solutions can be leveraged to build efficient and impactful analytics systems.

# Objective
The main objectives of this project are as follows:

- Develop a Near Real-Time Data Pipeline: Utilize Google Cloud Platform (GCP) tools to build a robust data pipeline that extracts cryptocurrency data from the CoinGecko API every 10 minutes, 
  ingesting it into Google Cloud Storage (GCS).
- Data Transformation and Warehousing: Process and transform raw data from GCS using Dataproc, load it into Google BigQuery as the central data warehouse, and archive the raw data back to GCS for backup and future reference.
- End-to-End Automation: Automate and orchestrate the entire pipeline using Apache Airflow running on Cloud Composer to ensure seamless, repeatable workflows.
- Data Visualization: Leverage Looker to create insightful visualizations, enabling users to understand trends and make data-driven decisions.
  
This project showcases an end-to-end data engineering solution for real-time cryptocurrency analytics using GCP tools.

# Architectural Solution

The diagram below showcases the architectural solution built using cloud technologies with automation at its core. This architecture is optimized for processing near real-time data and efficiently loading transformed data into BigQuery in batches. It is designed to ensure scalability, performance, and cost-effectiveness by leveraging the advanced capabilities of cloud infrastructure to minimize operational expenses while maximizing efficiency.

   ![Crypto_Arch](https://github.com/user-attachments/assets/d3f65c18-a511-4cd2-a516-2b9a8867929d)

Terraform is used as an Infrastructure as Code (IaC) tool, enabling the automated provisioning and management of cloud resources such as Google Cloud Storage (GCS) buckets and BigQuery tables. By defining infrastructure configurations in code, Terraform ensures consistent, repeatable deployments, which enhances collaboration and reduces the risk of manual errors.

Apache Airflow, running on Cloud Composer, acts as the workflow orchestration tool in this architecture. It streamlines the execution and monitoring of data workflows, allowing for the creation of complex data pipelines with built-in error handling and retry mechanisms. This ensures tasks are executed in the correct sequence and are easily monitored for performance.

In the following section, we will explore other tools and technologies that further complement this architecture

# Data Pipeline

A data pipeline is a series of data processing steps that automate the movement and transformation of data from various sources to a destination, typically a data warehouse or data lake. It ensures that data is collected, processed, and made available for analysis in a timely and efficient manner, allowing organizations to derive insights and make informed decisions based on up-to-date information.

- Data Extraction: This automated pipeline is designed to efficiently handle near-real-time data extraction. Raw data is fetched from the CoinGecko API every 10 minutes. An Airflow DAG has been created to manage and automate this process, ensuring reliable data retrieval. Below is a graphical representation of this DAG in Airflow.
   ![API_Extraction](https://github.com/user-attachments/assets/146748f4-0185-4ce6-844b-df92de5fa6fe)
  
- Transformations: Data transformation is performed using a DataProc cluster, a fully managed cloud service provided by Google Cloud that enables efficient, scalable processing of big data using Apache Spark and Hadoop. It simplifies cluster management, scaling, and integration with other Google Cloud Platform (GCP) services. This transformation process is orchestrated through an Airflow DAG, which is executed every 7 hours. The first task in the DAG creates the DataProc cluster. Once the cluster is operational, a job is submitted using a Python script stored in a GCS bucket to transform the raw data according to the specified job. After the transformation, the job loads the processed data into BigQuery in batches. Once the transformation and loading tasks are complete, the DAG triggers another task to delete the DataProc cluster. Deleting the cluster after each execution helps reduce costs by avoiding charges for idle resources. Finally, the last task of the DAG moves the raw data files that were processed by the DataProc cluster into an archive bucket for future reference, ensuring data preservation. Please refer below to see the screenshot of graphical representation of this dag. 
   ![Screenshot 2024-11-23 at 7 42 34 PM](https://github.com/user-attachments/assets/5c263861-1404-4da5-ba18-3eaecb86598e)





