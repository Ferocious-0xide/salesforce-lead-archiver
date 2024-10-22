# Salesforce-like Lead Data Archiver Script

This Python script archives "IsDeleted" records from a Postgres database with a Salesforce-like Lead structure to another Postgres database. It's designed to run continuously and mirrors the structure of a Salesforce Lead object.

## Prerequisites

- Python 3.7+
- Heroku CLI
- Git

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root with the following content:
   ```
   SOURCE_DATABASE_URL=<your-source-database-url>
   DESTINATION_DATABASE_URL=<your-destination-database-url>
   ```

## Modifying the Script

The script is currently set up to work with a Salesforce-like Lead object. If you need to modify the structure:

1. Open `data_archiver.py`
2. Locate the `LEAD_OBJECT` dictionary
3. Modify the fields, table name, or conditions as needed:
   ```python
   LEAD_OBJECT = {
       'table_name': 'your_table_name',
       'fields': ['Field1', 'Field2', ...],
       'condition': 'IsDeleted = TRUE',
       'upsert_field': 'External_ID__c'
   }
   ```

## Deployment to Heroku

1. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```

2. Set environment variables:
   ```
   heroku config:set SOURCE_DATABASE_URL=<your-source-database-url>
   heroku config:set DESTINATION_DATABASE_URL=<your-destination-database-url>
   ```

3. Deploy the app:
   ```
   git push heroku main
   ```

4. Scale the worker dyno:
   ```
   heroku ps:scale worker=1
   ```

## Maintenance

- Monitor the app logs:
  ```
  heroku logs --tail
  ```

- Update dependencies:
  Periodically update `requirements.txt` and redeploy.

- Scaling:
  To handle larger datasets, you may need to adjust the polling interval in the script and scale the Heroku dyno:
  ```
  heroku ps:scale worker=2
  ```

## Next Steps

1. Create a Heroku Button for easy deployment
2. Develop a user interface for easy configuration and monitoring

## Support

For issues or feature requests, please open an issue in the GitHub repository.