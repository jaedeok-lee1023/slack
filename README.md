name: slack CI

on:
  workflow_dispatch:
  schedule:
  - cron: "0 15 * * *" # 세계 표준시 기준으로 01시는 한국시간 오전 10시
  
jobs:
  post_announcement_message:
    runs-on: ubuntu-latest
    steps:
      - name: action code checkout
        uses: actions/checkout@v3
      - name: Set up Python 3.10
      
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
          
      - name: Install python dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          
      - name: run main.py
        env:
          SLACK_TOKEN: ${{ secrets.SLACK_TOKEN }}
          SLACK_CHANNEL: ${{ secrets.SLACK_CHANNEL }}
        run: python3 main.py
