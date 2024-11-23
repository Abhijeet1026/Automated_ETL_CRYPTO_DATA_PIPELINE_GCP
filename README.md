# Data Engineering:Automated Crypto Data Pipeline GCP
1. [Introduction](#introduction)
2. [Objective](#objective)
3. [Architectural Solution](#architectural-solution)
4. [Data Pipeline](#Data-Pipeline)
   - Ingestion
   - Processing
   - Tranformations
5. [Visualization](#Visualization) 
6. [Summary](#Summary)
7. [Reference](#reference)

# Introduction
The Automated Crypto Data Pipeline and Analytics project focuses on building a robust data pipeline using Google Cloud Platform (GCP) tools to extract, process, and analyze cryptocurrency data from the [CoinGecko](https://docs.coingecko.com/reference/coins-markets) API. CoinGecko, a widely used platform, provides real-time information on various cryptocurrencies, capturing key metrics such as prices, market capitalization, trading volumes, and supply data.

At the heart of this project is a fully automated data pipeline that seamlessly ingests high-frequency crypto data in near real-time. Using GCP tools like Cloud Storage, Cloud Composer, Dataproc, and BigQuery, the pipeline performs efficient data extraction, transformation, and loading (ETL). This setup ensures scalability and reliability, handling large volumes of cryptocurrency data without performance bottlenecks.

The pipeline not only processes raw data but transforms it into meaningful insights, such as identifying the current prices, total supply, trading volumes, and market capitalizations of top-performing coins. This comprehensive approach enables users to understand cryptocurrency trends and make data-driven decisions in an ever-changing market.

By combining the power of the CoinGecko API with the scalability of GCP's data tools, this project demonstrates how cloud-based solutions can be leveraged to build efficient and impactful analytics systems.
