terraform {
  required_version = ">= 1.0"
  backend "local" {} # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region

}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket1" {
  name     = "${var.project}_${local.data_lake_bucket_raw}" # Concatenating DL bucket & Project name for unique naming
  location = var.region

    # Optional, but recommended settings:
  storage_class               = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 60 // days
    }
  }

  force_destroy = true
}

resource "google_storage_bucket" "data-lake-bucket2" {
  name     = "${var.project}_${local.data_lake_bucket_archieve}" # Concatenating DL bucket & Project name for unique naming
  location = var.region

    # Optional, but recommended settings:
  storage_class               = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 60 // days
    }
  }

  force_destroy = true
}

#https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "crypto_de" {
  dataset_id = var.bq_dataset
  project    = var.project
  location   = var.region
}

#https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table

resource "google_bigquery_table" "crypto_de" {
  dataset_id = google_bigquery_dataset.crypto_de.dataset_id
  table_id   = "crypto_data"

  schema              = <<EOF
  [
    {
      "name": "id",
      "type" : "STRING",
      "mode" : "NULLABLE",
      "description": "Unique id of the crypto currency"
    },
    {
      "name": "symbol",
      "type" : "STRING",
      "mode" : "NULLABLE",
      "description": "symbol of crypto currency"
    },
    {
      "name": "name",
      "type" : "STRING",
      "mode" : "NULLABLE",
      "description": "name of the crypto currency"
    },

     {
      "name": "current_price",
      "type" : "FLOAT",
      "mode" : "NULLABLE",
      "description": "current price of the crypto currency"
    },
     {
      "name": "market_cap",
      "type" : "FLOAT64",
      "mode" : "NULLABLE",
      "description": "current price of the crypto currency"
    },
   
      {
      "name": "market_cap_rank",
      "type" : "INT64",
      "mode" : "NULLABLE",
      "description": "market cap rank of the crypto currency"
    },
     {
      "name": "total_volume",
      "type" : "FLOAT64",
      "mode" : "NULLABLE",
      "description": "total volumeof crypto currency"
    },
    {
      "name": "high_24h",
      "type" : "FLOAT64",
      "mode" : "NULLABLE",
      "description": "Highest value in last 24 hour of crypto currency"
    },
    {
      "name": "low_24h",
      "type" : "FLOAT64",
      "mode" : "NULLABLE",
      "description": "lowest value in last 24 hour of crypto currency"
    },
    {
      "name": "total_supply",
      "type" : "FLOAT64",
      "mode" : "NULLABLE",
      "description": "total supply in last 24 hour of crypto currency"
    },
      {
      "name": "price_change_percentage_24h",
      "type" : "FLOAT64",
      "mode" : "NULLABLE",
      "description": "price percentage of the crypto currency"
    },
     {
      "name": "circulating_supply",
      "type" : "FLOAT64",
      "mode" : "NULLABLE",
      "description": "circulating supply of crypto currency"
    },
       {
      "name": "max_supply",
      "type" : "FLOAT64",
      "mode" : "NULLABLE",
      "description": "max supply of crypto currency"
    },
    {
      "name": "last_updated",
      "type" : "TIMESTAMP",
      "mode" : "NULLABLE",
      "description": "Last updated time stamp"
    },
    {
      "name": "ingestion_timestamp",
      "type" : "TIMESTAMP",
      "mode" : "NULLABLE",
      "description": "ingestion_timestamp"
    }
  ] 
  EOF
  deletion_protection = false #will delete the dataset with the table using terrafrom destroy command
}