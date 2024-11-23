locals {
  data_lake_bucket_raw = "crypto_data_raw"
  data_lake_bucket_archieve = "crypto_data_archieve"

}



variable "project" {
  description = "Your GCP project ID"
  default     = "dataengineering1-433721"
  
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default     = "us-central1"
  type        = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "STANDARD"
}

variable "bq_dataset" {
  description = "BigQuery Dataset:  data (from GCS) will be written to"
  type        = string
  default     = "crypto_de"
}