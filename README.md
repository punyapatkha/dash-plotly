## How it Works

This example uses of Dash Plotly deploy on Serverless Functions.

integrate with SQL Database and Langchain

## Ovewview Architect Diagram

![alt text](https://github.com/punyapatkha/dash-plotly/blob/main/assets/overview-architect-2.png)

## ER Diagram

![alt text](https://github.com/punyapatkha/dash-plotly/blob/main/assets/er-diagarm.png)


## Demo

[https://dash-plotly-5d29.onrender.com/](https://dash-plotly-5d29.onrender.com/)

## Current Functionaliy

- Basic Authentication
- Basic Callback

#### Summary Page

- Fetch data directly from PostgreSQL with callback and filter

#### Chat Bot Page

- Query question with response base from information in database

## Page

#### Summary Page

![alt text](https://github.com/punyapatkha/dash-plotly/blob/main/assets/example_page_1.png)

![alt text](https://github.com/punyapatkha/dash-plotly/blob/main/assets/example_page_2.png)

#### Chat Bot Page

![alt text](https://github.com/punyapatkha/dash-plotly/blob/main/assets/example_page_3.png)

![alt text](https://github.com/punyapatkha/dash-plotly/blob/main/assets/example_page_4.png)

## How to Deploy on Render

1.Create postgres database

2.Run migrate.py to generate random data for mockup

3.Get openAI API token

4.deploy to Render and add environment variable for database and OpenAI API

5.Set up cron-tab to wake Render serverless function


## Running Locally
1.Create postgres database

2.Run migrate.py to generate random data for mockup

3.Get openAI API token

4.Add Environment variable to .env file for database and OpenAI API

5.Run following command
```
pip install -r requirement.txt

python app.py
```

