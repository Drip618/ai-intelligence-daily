#!/bin/bash
# deploy/local/run.sh - Run agent locally with scheduler

set -e

echo "Starting AI Intelligence Agent..."

# Install dependencies
pip install -r requirements.txt

# Install playwright browsers if needed
playwright install --with-deps chromium

# Run agent immediately once
python -m src.core.agent --run-once

# Set up cron job for daily execution
(crontab -l 2>/dev/null; echo "0 9 * * * cd $(pwd) && python -m src.core.agent --run-once") | crontab -

echo "Agent scheduled for daily execution at 9:00 AM"
