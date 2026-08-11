# Quantitative Trading Pipeline

A robust, modular, and cloud-native algorithmic trading system built in Python. Designed for high reliability, this pipeline orchestrates market data ingestion, machine-learning-based regime detection, multi-strategy arbitration, and risk-adjusted order execution targeting the **XT.com** exchange.

## Core Features
*   **Modular Architecture:** Strict separation of concerns across Data, Features, Strategy, Risk, and Execution layers.
*   **Machine Learning Integration:** Hidden Markov Model (HMM) integration for dynamic market regime detection.
*   **Stateless Cloud Execution:** Ephemeral-ready architecture using **Supabase** (PostgreSQL) for persistent state management and execution idempotency.
*   **Multi-Venue Support:** Interface-driven adapter pattern currently supporting XT.com (REST) and MetaTrader 5.
*   **Automated Orchestration:** Fully containerized via Docker and automated via GitHub Actions cron schedules.

## Prerequisites
*   Python 3.11+
*   XT.com API Key and Secret Key
*   Supabase Account and Database URL
*   Docker (Optional, for containerized deployment)

## Quick Start

### 1. Installation
Clone the repository and install the required dependencies:
```bash
git clone <repository_url>
cd quant-trading-pipeline
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt