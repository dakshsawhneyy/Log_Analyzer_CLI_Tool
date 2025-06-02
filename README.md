# Log Analyzer CLI Tool 

A lightweight Python-based CLI tool to parse and analyze log files for critical alerts and generate summaries. Ideal for system administrators, DevOps engineers, and developers who need fast, scriptable insights from log data.

---

## Features

- Parse and scan log files for common alert keywords
- Generate readable summaries with timestamped stats
- Optional email alerts on critical issues (SMTP via Gmail)
- Save summaries to `summary.json` for audit history
- Beep alert support for immediate attention
- Built-in shell script (`monitor.sh`) to simulate log generation

---

##  Technologies Used

- Python 3
- Shell scripting (`bash`)
- `argparse`, `smtplib`, `email`, `json`, `collections` modules
- Gmail SMTP for alerting

---

## 📂 Directory Structure

```
.
├── log_analyzer.py        # Main CLI script
├── monitor.sh             # Shell script to generate dummy logs
├── summary.json           # Stores all saved summaries (if --save-summary is used)
└── sample.log             # (Optional) Sample log file structure for reference
```

---

##  How to Use

### 1. Run Shell Script (Optional)
```bash
chmod +x monitor.sh
./monitor.sh > system.log
```

### 2. Analyze Logs
```bash
python log_analyzer.py -f system.log --save-summary --get-email --get-beep
```

### 3. CLI Flags

| Flag | Description |
|------|-------------|
| `-f, --file` | Path to the log file to analyze (**required**) |
| `-k, --keywords` | Keywords to look for (default: `warn`, `error`, `fail`, `critical`) |
| `--save-summary` | Save the results to `summary.json` |
| `--get-email` | Send an email if alerts are found |
| `--get-beep` | Play a beep sound if alerts are found |

> Ensure you set your Gmail credentials via environment variables:  
> `EMAIL_ADDRESS`, `EMAIL_PASSWORD`

---

##  Security Notes

-  Do **NOT** commit log files to GitHub. Add them to `.gitignore`
-  Keep your SMTP credentials secure (use `.env` or CI secrets)
-  Consider using a mock or sanitized log sample for public sharing

---

##  Future Improvements

- Add GUI support
- Integrate Slack/Discord alert channels
- Log file rotation handling

---

##  Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss.

---

## 🧑‍💻 Author

**Daksh Sawhney**  
DevOps & Cloud Enthusiast | AWS | Kubernetes | Python

---
