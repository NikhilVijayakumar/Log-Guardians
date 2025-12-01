# Log Guardians - Automated Log Analysis Pipeline

An AI-powered log analysis system that automatically processes logs, detects anomalies, and generates security reports.

## Features

- **Automated Log Processing**: Chunks and converts raw logs into structured JSON
- **AI-Powered Anomaly Detection**: Uses LLM reasoning to identify security threats and system failures
- **Consolidated Reporting**: Generates comprehensive security reports with actionable recommendations
- **Platform Agnostic**: Works with logs from Linux, Windows, Cloud platforms, and more

## Pipeline Architecture

```
Raw Logs → Chunking → JSON Conversion → Anomaly Detection → Final Report
```

### Components

1. **Log Chunker**: Splits large log files into manageable chunks
2. **JSON Converter Agent**: Converts raw logs into structured JSON format
3. **Anomaly Detection Agent**: Analyzes JSON logs and identifies anomalies
4. **Report Generator Agent**: Aggregates findings and creates a consolidated report

## Quick Start

### Prerequisites

- Python 3.10+
- Virtual environment activated
- Google API key configured in `.env`

### Running the Full Pipeline

```bash
# From project root
python src/log/guardians/app/main/main.py
```

This single command will:
1. Generate and chunk logs based on `chunker_config.yaml`
2. Convert all chunks to structured JSON
3. Analyze each JSON file for anomalies
4. Generate `FINAL_ANOMALY_REPORT.md`

### Running Individual Agents

You can also run each agent separately:

```bash
# JSON Conversion only
python src/log/guardians/app/agent/json_converter_agent.py

# Anomaly Detection only
python src/log/guardians/app/agent/anomaly_detection_agent.py

# Report Generation only
python src/log/guardians/app/agent/report_generator_agent.py
```

## Configuration

Edit `src/log/guardians/app/main/config/chunker_config.yaml` to configure:

- `active_profile`: Log type (e.g., 'syslog', 'hpc')
- `input_log_file`: Path to your raw log file
- `chunk_size`: Number of log entries per chunk

## Output Structure

```
.LogGuardians/
├── output/
│   └── logs/
│       └── {profile}/
│           └── {log_name}/
│               ├── chunk_0000.log
│               ├── chunk_0001.log
│               └── ...
├── output_json_structured_logs/
│   ├── chunk_0000.json
│   ├── chunk_0001.json
│   └── ...
└── output_anomalies/
    ├── chunk_0000_anomaly.json (only if anomalies found)
    ├── chunk_0001_anomaly.json
    └── ...

FINAL_ANOMALY_REPORT.md  # Consolidated security report
```

## Anomaly Detection

The system detects:

- **Security Threats**: Brute force attacks, unauthorized access attempts
- **System Failures**: Service crashes, hardware warnings
- **Anomalous Behavior**: Unusual activity patterns, time spikes

Anomalies are classified by severity:
- Critical
- High
- Medium
- Low

## Report Format

The final report includes:

- **Executive Summary**: High-level security posture overview
- **Critical Threats**: Most severe issues requiring immediate attention
- **Pattern Analysis**: Recurring attacks or failures
- **Detailed Findings**: Grouped by severity
- **Actionable Recommendations**: Prioritized mitigation steps

## Development

### Project Structure

```
src/log/guardians/app/
├── main/
│   ├── main.py              # Pipeline orchestrator
│   └── config/
│       └── chunker_config.yaml
├── agent/
│   ├── json_converter_agent.py
│   ├── anomaly_detection_agent.py
│   ├── report_generator_agent.py
│   └── tools.py             # Shared tools
└── features/
    └── chunking/
        └── chunker.py
```

### Adding New Log Types

1. Add a new profile in `chunker_config.yaml`
2. Define the log start regex pattern
3. Update `active_profile` to your new profile
4. Run the pipeline

## License

# Log Guardians - Automated Log Analysis Pipeline

An AI-powered log analysis system that automatically processes logs, detects anomalies, and generates security reports.

## Features

- **Automated Log Processing**: Chunks and converts raw logs into structured JSON
- **AI-Powered Anomaly Detection**: Uses LLM reasoning to identify security threats and system failures
- **Consolidated Reporting**: Generates comprehensive security reports with actionable recommendations
- **Platform Agnostic**: Works with logs from Linux, Windows, Cloud platforms, and more

## Pipeline Architecture

```
Raw Logs → Chunking → JSON Conversion → Anomaly Detection → Final Report
```

### Components

1. **Log Chunker**: Splits large log files into manageable chunks
2. **JSON Converter Agent**: Converts raw logs into structured JSON format
3. **Anomaly Detection Agent**: Analyzes JSON logs and identifies anomalies
4. **Report Generator Agent**: Aggregates findings and creates a consolidated report

## Quick Start

### Prerequisites

- Python 3.10+
- Virtual environment activated
- Google API key configured in `.env`

### Running the Full Pipeline

```bash
# From project root
python src/log/guardians/app/main/main.py
```

This single command will:
1. Generate and chunk logs based on `chunker_config.yaml`
2. Convert all chunks to structured JSON
3. Analyze each JSON file for anomalies
4. Generate `FINAL_ANOMALY_REPORT.md`

### Running Individual Agents

You can also run each agent separately:

```bash
# JSON Conversion only
python src/log/guardians/app/agent/json_converter_agent.py

# Anomaly Detection only
python src/log/guardians/app/agent/anomaly_detection_agent.py

# Report Generation only
python src/log/guardians/app/agent/report_generator_agent.py
```

## Configuration

Edit `src/log/guardians/app/main/config/chunker_config.yaml` to configure:

- `active_profile`: Log type (e.g., 'syslog', 'hpc')
- `input_log_file`: Path to your raw log file
- `chunk_size`: Number of log entries per chunk

## Output Structure

```
.LogGuardians/
├── output/
│   └── logs/
│       └── {profile}/
│           └── {log_name}/
│               ├── chunk_0000.log
│               ├── chunk_0001.log
│               └── ...
├── output_json_structured_logs/
│   ├── chunk_0000.json
│   ├── chunk_0001.json
│   └── ...
└── output_anomalies/
    ├── chunk_0000_anomaly.json (only if anomalies found)
    ├── chunk_0001_anomaly.json
    └── ...

FINAL_ANOMALY_REPORT.md  # Consolidated security report
```

## Anomaly Detection

The system detects:

- **Security Threats**: Brute force attacks, unauthorized access attempts
- **System Failures**: Service crashes, hardware warnings
- **Anomalous Behavior**: Unusual activity patterns, time spikes

Anomalies are classified by severity:
- Critical
- High
- Medium
- Low

## Report Format

The final report includes:

- **Executive Summary**: High-level security posture overview
- **Critical Threats**: Most severe issues requiring immediate attention
- **Pattern Analysis**: Recurring attacks or failures
- **Detailed Findings**: Grouped by severity
- **Actionable Recommendations**: Prioritized mitigation steps

## Development

### Project Structure

```
src/log/guardians/app/
├── main/
│   ├── main.py              # Pipeline orchestrator
│   └── config/
│       └── chunker_config.yaml
├── agent/
│   ├── json_converter_agent.py
│   ├── anomaly_detection_agent.py
│   ├── report_generator_agent.py
│   └── tools.py             # Shared tools
└── features/
    └── chunking/
        └── chunker.py
```

### Adding New Log Types

1. Add a new profile in `chunker_config.yaml`
2. Define the log start regex pattern
3. Update `active_profile` to your new profile
4. Run the pipeline

## License

# Log Guardians - Automated Log Analysis Pipeline

An AI-powered log analysis system that automatically processes logs, detects anomalies, and generates security reports.

## Features

- **Automated Log Processing**: Chunks and converts raw logs into structured JSON
- **AI-Powered Anomaly Detection**: Uses LLM reasoning to identify security threats and system failures
- **Consolidated Reporting**: Generates comprehensive security reports with actionable recommendations
- **Platform Agnostic**: Works with logs from Linux, Windows, Cloud platforms, and more

## Pipeline Architecture

```
Raw Logs → Chunking → JSON Conversion → Anomaly Detection → Final Report
```

### Components

1. **Log Chunker**: Splits large log files into manageable chunks
2. **JSON Converter Agent**: Converts raw logs into structured JSON format
3. **Anomaly Detection Agent**: Analyzes JSON logs and identifies anomalies
4. **Report Generator Agent**: Aggregates findings and creates a consolidated report

## Quick Start

### Prerequisites

- Python 3.10+
- Virtual environment activated
- Google API key configured in `.env`

### Running the Full Pipeline

```bash
# From project root
python src/log/guardians/app/main/main.py
```

This single command will:
1. Generate and chunk logs based on `chunker_config.yaml`
2. Convert all chunks to structured JSON
3. Analyze each JSON file for anomalies
4. Generate `FINAL_ANOMALY_REPORT.md`

### Running Individual Agents

You can also run each agent separately:

```bash
# JSON Conversion only
python src/log/guardians/app/agent/json_converter_agent.py

# Anomaly Detection only
python src/log/guardians/app/agent/anomaly_detection_agent.py

# Report Generation only
python src/log/guardians/app/agent/report_generator_agent.py
```

## Configuration

Edit `src/log/guardians/app/main/config/chunker_config.yaml` to configure:

- `active_profile`: Log type (e.g., 'syslog', 'hpc')
- `input_log_file`: Path to your raw log file
- `chunk_size`: Number of log entries per chunk

## Output Structure

```
.LogGuardians/
├── output/
│   └── logs/
│       └── {profile}/
│           └── {log_name}/
│               ├── chunk_0000.log
│               ├── chunk_0001.log
│               └── ...
├── output_json_structured_logs/
│   ├── chunk_0000.json
│   ├── chunk_0001.json
│   └── ...
└── output_anomalies/
    ├── chunk_0000_anomaly.json (only if anomalies found)
    ├── chunk_0001_anomaly.json
    └── ...

FINAL_ANOMALY_REPORT.md  # Consolidated security report
```

## Anomaly Detection

The system detects:

- **Security Threats**: Brute force attacks, unauthorized access attempts
- **System Failures**: Service crashes, hardware warnings
- **Anomalous Behavior**: Unusual activity patterns, time spikes

Anomalies are classified by severity:
- Critical
- High
- Medium
- Low

## Report Format

The final report includes:

- **Executive Summary**: High-level security posture overview
- **Critical Threats**: Most severe issues requiring immediate attention
- **Pattern Analysis**: Recurring attacks or failures
- **Detailed Findings**: Grouped by severity
- **Actionable Recommendations**: Prioritized mitigation steps

## Development

### Project Structure

```
src/log/guardians/app/
├── main/
│   ├── main.py              # Pipeline orchestrator
│   └── config/
│       └── chunker_config.yaml
├── agent/
│   ├── json_converter_agent.py
│   ├── anomaly_detection_agent.py
│   ├── report_generator_agent.py
│   └── tools.py             # Shared tools
└── features/
    └── chunking/
        └── chunker.py
```

### Adding New Log Types

1. Add a new profile in `chunker_config.yaml`
2. Define the log start regex pattern
3. Update `active_profile` to your new profile
4. Run the pipeline

## License

Apache 2.O
