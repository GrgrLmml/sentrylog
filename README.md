# SentryLog

## Overview
SentryLog is a Python-based application that taps directly into the logs of running Docker containers without requiring any modifications to the containers themselves. It's a real-time log monitoring tool designed to assist developers by reducing the effort needed to monitor logs and detect patterns that might otherwise go unnoticed.

![SentryLog](resources/app.jpeg)

The application leverages the latest advances in AI, with connectors currently implemented for Anthropic and Groq. This AI-powered analysis provides an additional layer of insight into your container activities.

The results of the AI analysis are logged to Slack, providing an easily accessible and real-time overview of what happens in your deployment. SentryLog is not intended to replace developers monitoring logs but rather to serve as a helpful tool that enhances the efficiency and effectiveness of log monitoring.

SentryLog is in its early stages and currently monitors Nginx logs. Contributions to expand its capabilities are welcome.

## Requirements
- Anthropic Claude or Groq API key (for AI analysis)
- Slack token for your organization (for logging results)
- A deployment that runs nginx, otherwise you won't see any logs ;-)

## Getting Started

### Prerequisites
Setup the following environment variables:
- `ANTHROPIC_API_KEY` or `GROQ_API_KEY`: Your API key for AI analysis
- `ANTHROPIC_MODEL_ID` or `GROQ_MODEL_ID`: The model ID for the AI analysis (default is `claude-3-haiku-20240307` for Anthropic and `mixtral-8x7b-32768` for Groq)
- `SLACK_TOKEN`: Your Slack token
- `SLACK_CHANNEL`: The Slack channel where you want to log the results

### Building and Running SentryLog
1. **Clone from git and run directly **
   
   Clone this repository to your local machine:
   ```bash
   git clone git@github.com:GrgrLmml/sentrylog.git
   cd sentrylog
   pip install -r requirements.txt
   python src/sentry.py
   ```

2. **Pull from Docker Hub**
  The image is available on Docker Hub, so you can pull it directly:
    ```bash
    docker pull grgrlmml/sentrylog:latest
   ```
3. **Add the service to your `docker-compose.yml`**
    
    Add SentryLog to your existing `docker-compose.yml` file:
    ```yaml
    version: '3.8'
    services:
      sentrylog:
         image: grgrlmml/sentrylog:latest
         volumes:
            - /var/run/docker.sock:/var/run/docker.sock
         environment:
            - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
            - ANTHROPIC_MODEL_ID=${ANTHROPIC_MODEL_ID}
            - GROQ_API_KEY=${GROQ_API_KEY}
            - GROQ_MODEL_ID=${GROQ_MODEL_ID}
            - SLACK_TOKEN=your-slack-token
            - SLACK_CHANNEL=your-slack-channel
         restart: always
    ```
### Running SentryLog with a Custom Template
To use a custom prompt template, mount a volume containing your template file when running the Docker container:

```yaml
volumes:
  - ./path/to/your/template.md:/usr/src/app/templates/custom.md
```
Make sure to set the `TEMPLATE` environment variable to the name of your custom template file (e.g., `custom.md`).
### Running SentryLog with a Custom Container Name
By default, SentryLog monitors the logs of a container with a name containing 'nginx'. To monitor a different container, set the `CONTAINER_TO_WATCH` environment variable when running the Docker container:
    
```yaml
environment:
  - CONTAINER_TO_WATCH=your-container-name
```
Replace `your-container-name` with the name of the container you want to monitor. SentryLog will search for a container whose name contains the specified value.


## Usage
Once SentryLog is running, it will start monitoring the logs. The AI analysis results will be logged to the specified Slack channel.

## Contributing
Contributions to this project are welcome. Please ensure to follow best practices and provide tests for new features.

