---
name: kaggle-api-expert
description: Expert agent for Kaggle API authentication, dataset management, and running Kaggle notebooks on Texas Tech HPCC. Specializes in connecting Jupyter notebooks to Kaggle API and submitting to code competitions. Always checks VPN connection first before HPCC operations.
---

# Kaggle API Expert

This agent specializes in Kaggle API operations, dataset management, and running Kaggle notebooks on Texas Tech HPCC (High Performance Computing Center). The agent understands authentication, dataset creation, competition submissions, and HPCC-specific configurations.

## Purpose and Scope

Help users with:
- **Kaggle API Authentication**: Setting up and configuring Kaggle API credentials
- **Dataset Management**: Creating, uploading, and managing Kaggle datasets
- **HPCC Integration**: Running Kaggle notebooks on Texas Tech HPCC infrastructure
- **Jupyter Integration**: Connecting Jupyter notebooks to Kaggle API
- **Competition Submissions**: Submitting to Kaggle code competitions
- **VPN Verification**: Ensuring VPN connection before HPCC operations

## Target Location

This skill is project-specific and should be stored at:
- `.cursor/skills/kaggle-api-expert/` (in the spring-2026 project)

## Trigger Scenarios

Automatically apply this skill when users request:
- Kaggle API setup or authentication
- Creating or managing Kaggle datasets
- Running Kaggle notebooks on HPCC
- Connecting Jupyter notebooks to Kaggle API
- Submitting to Kaggle competitions
- HPCC Jupyter notebook setup

## Prerequisites Check: VPN Connection

**CRITICAL**: Before any HPCC operations, always verify VPN connection:

1. **Ask the user**: "Are you connected to the Texas Tech VPN?"
2. **Verify connection**: User must be connected to TTU VPN to access HPCC resources
3. **If not connected**: Provide VPN connection instructions before proceeding

**HPCC Access Requirements**:
- Texas Tech VPN connection (required)
- TTU credentials for HPCC access
- Jupyter notebook access on HPCC

## Key Domain Knowledge

### Kaggle API Authentication

The agent understands:
- **API Credentials**: `kaggle.json` file format and location
- **Token Management**: Using Kaggle username and API token
- **Environment Setup**: Setting up Kaggle API in various environments
- **Authentication Methods**: Credential file vs. environment variables

### Dataset Operations

The agent understands:
- **Creating Datasets**: Creating new datasets via API
- **Uploading Data**: Uploading files and metadata
- **Version Management**: Managing dataset versions
- **Privacy Settings**: Public, private, and organization datasets

### HPCC-Specific Knowledge

The agent understands:
- **HPCC Jupyter Setup**: Accessing Jupyter notebooks on HPCC
- **VPN Requirements**: Always check VPN before HPCC access
- **Resource Allocation**: Understanding HPCC compute resources
- **Data Storage**: HPCC filesystem and data management
- **Module Loading**: Loading software modules on HPCC

### Competition Submissions

The agent understands:
- **Downloading Competitions**: Getting competition data
- **Creating Notebooks**: Setting up Kaggle notebooks
- **Submitting Predictions**: Submitting results to competitions
- **Leaderboard Access**: Checking competition standings

## Kaggle API Setup

### Step 1: Verify VPN Connection (HPCC Only)

**IMPORTANT**: If working with HPCC, verify VPN connection first:

```
Before proceeding, please confirm:
- Are you connected to the Texas Tech VPN?
- Can you access HPCC resources?
```

### Step 2: Get Kaggle API Credentials

1. **Log in to Kaggle**: Visit [https://www.kaggle.com/](https://www.kaggle.com/)
2. **Navigate to Account**: Click your profile → Account tab
3. **Create API Token**: Scroll to "API" section → Click "Create New Token"
4. **Download `kaggle.json`**: Save the file (contains username and key)

### Step 3: Install Kaggle API

```bash
# Install Kaggle API package
pip install kaggle

# Or using conda
conda install -c conda-forge kaggle
```

### Step 4: Configure Credentials

**Option 1: Credential File (Recommended)**

```bash
# Create .kaggle directory
mkdir -p ~/.kaggle

# Move kaggle.json to .kaggle directory
mv ~/Downloads/kaggle.json ~/.kaggle/

# Set permissions (required by Kaggle)
chmod 600 ~/.kaggle/kaggle.json
```

**Option 2: Environment Variables**

```bash
export KAGGLE_USERNAME="your-username"
export KAGGLE_KEY="your-api-key"
```

**Option 3: For HPCC Jupyter**

When using Jupyter notebooks on HPCC, credentials should be placed in the home directory:

```bash
# On HPCC (after VPN connection)
mkdir -p ~/.kaggle
# Upload kaggle.json to ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

### Step 5: Verify Installation

```bash
kaggle --version
kaggle competitions list
```

## Creating Datasets

### Basic Dataset Creation

```bash
# Create a new dataset
kaggle datasets create -p /path/to/dataset

# With metadata file
kaggle datasets create -p /path/to/dataset -r zip
```

### Dataset Structure

```
dataset-directory/
├── data.csv
├── dataset-metadata.json
└── README.md
```

**dataset-metadata.json** example:

```json
{
  "title": "Dataset Title",
  "id": "username/dataset-name",
  "licenses": [{"name": "CC0-1.0"}]
}
```

### Uploading Dataset

```bash
# Create and upload dataset
kaggle datasets create -p /path/to/dataset -r zip
```

## HPCC Jupyter Setup

### Prerequisites (Check First!)

**CRITICAL**: Before HPCC operations:
1. ✅ **VPN Connection**: User must be connected to Texas Tech VPN
2. ✅ **HPCC Access**: User must have HPCC account and credentials
3. ✅ **Jupyter Access**: User must have Jupyter notebook access on HPCC

### Accessing HPCC Jupyter

1. **Connect to VPN**: Use Texas Tech VPN client
2. **Access HPCC Portal**: Visit [HPCC Jupyter Portal](https://jupyter.hpcc.ttu.edu/) (or check HPCC documentation)
3. **Launch Jupyter**: Start Jupyter notebook session
4. **Verify Network**: Ensure Kaggle API access from Jupyter environment

### Installing Kaggle API in HPCC Jupyter

```python
# In Jupyter notebook cell
!pip install kaggle --user

# Verify installation
!kaggle --version
```

### Setting Up Credentials in HPCC Jupyter

```python
# Option 1: Upload kaggle.json via Jupyter file browser
# Place in ~/.kaggle/kaggle.json

# Option 2: Set environment variables in notebook
import os
os.environ['KAGGLE_USERNAME'] = 'your-username'
os.environ['KAGGLE_KEY'] = 'your-api-key'

# Option 3: Create kaggle.json programmatically (be careful with security)
import json
kaggle_creds = {
    "username": "your-username",
    "key": "your-api-key"
}
os.makedirs('/home/username/.kaggle', exist_ok=True)
with open('/home/username/.kaggle/kaggle.json', 'w') as f:
    json.dump(kaggle_creds, f)
os.chmod('/home/username/.kaggle/kaggle.json', 0o600)
```

## Using Kaggle API in Jupyter Notebooks

### Downloading Competition Data

```python
import kaggle

# Download competition dataset
!kaggle competitions download -c competition-name

# Extract files
import zipfile
with zipfile.ZipFile('competition-name.zip', 'r') as zip_ref:
    zip_ref.extractall('./data')
```

### Downloading Public Datasets

```python
# Download dataset
!kaggle datasets download -d username/dataset-name

# Extract
import zipfile
with zipfile.ZipFile('dataset-name.zip', 'r') as zip_ref:
    zip_ref.extractall('./data')
```

### Submitting to Competitions

```python
# Submit predictions
!kaggle competitions submit -c competition-name -f predictions.csv -m "Submission message"

# Check leaderboard
!kaggle competitions leaderboard competition-name --show
```

## Competition Workflow

### Complete Competition Submission Process

1. **Find Competition**: Browse [Kaggle Competitions](https://www.kaggle.com/competitions)

2. **Download Dataset**:
   ```bash
   kaggle competitions download -c competition-name
   ```

3. **Create Kaggle Notebook**:
   - Via web interface at kaggle.com
   - Or use Kaggle API to create programmatically

4. **Write Code**:
   - Develop model/algorithm in notebook
   - Test locally or on HPCC

5. **Submit Predictions**:
   ```bash
   kaggle competitions submit -c competition-name \
     -f predictions.csv \
     -m "Model description"
   ```

6. **Check Score**:
   ```bash
   kaggle competitions leaderboard competition-name
   ```

## HPCC-Specific Considerations

### Module Loading

HPCC uses environment modules. Load required modules:

```bash
# In Jupyter notebook or HPCC terminal
module load python/3.9  # Example version
module load cuda/11.8   # If using GPU
```

### Data Storage

- **Home Directory**: Limited space (~50GB)
- **Scratch Space**: `/scratch/username/` for temporary data
- **Dataset Storage**: Store large datasets in scratch space

### Resource Allocation

HPCC provides:
- **CPU nodes**: For general computing
- **GPU nodes**: For deep learning workloads
- **Memory**: Varies by allocation
- **Job Scheduling**: May use SLURM for job submission

## Troubleshooting

### Common Issues

#### 1. Authentication Errors

**Symptom**: `401 - Unauthorized` or `403 - Forbidden`

**Solutions**:
- Verify `kaggle.json` is in `~/.kaggle/`
- Check file permissions: `chmod 600 ~/.kaggle/kaggle.json`
- Verify credentials are correct (regenerate if needed)
- Check API token hasn't expired

#### 2. VPN Connection Issues (HPCC)

**Symptom**: Cannot access HPCC resources

**Solutions**:
- Verify VPN connection is active
- Check VPN credentials
- Ensure VPN client is properly configured
- Try reconnecting to VPN

#### 3. HPCC Access Denied

**Symptom**: Cannot access Jupyter portal

**Solutions**:
- Verify VPN is connected
- Check HPCC account is active
- Verify Jupyter access is enabled for your account
- Contact HPCC support if issues persist

#### 4. Kaggle API Not Found in Jupyter

**Symptom**: `kaggle: command not found` in Jupyter

**Solutions**:
```python
# Install with --user flag
!pip install kaggle --user

# Or add to system path
import sys
sys.path.append('/home/username/.local/bin')
```

#### 5. Permission Denied Errors

**Symptom**: Permission errors when accessing files

**Solutions**:
```bash
# Fix kaggle.json permissions
chmod 600 ~/.kaggle/kaggle.json

# Fix directory permissions
chmod 700 ~/.kaggle
```

## Best Practices

### Security

1. **Never commit `kaggle.json`** to version control
2. **Use environment variables** when possible
3. **Set proper file permissions**: `chmod 600` for credentials
4. **Regenerate tokens** if compromised

### HPCC Usage

1. **Always verify VPN** before HPCC operations
2. **Use scratch space** for large datasets
3. **Clean up temporary files** after jobs
4. **Respect resource limits** and quotas
5. **Monitor job status** and resource usage

### Dataset Management

1. **Include clear README** with dataset metadata
2. **Use version control** for dataset changes
3. **Document data sources** and preprocessing
4. **Set appropriate licenses**

## Reference Links

- **Kaggle API Documentation**: [https://github.com/Kaggle/kaggle-api](https://github.com/Kaggle/kaggle-api)
- **HPCC Jupyter Guide**: [https://www.depts.ttu.edu/hpcc/userguides/general_guides/jupyter-notebooks.php](https://www.depts.ttu.edu/hpcc/userguides/general_guides/jupyter-notebooks.php)
- **Kaggle Tutorials**: [https://github.com/Kaggle/kaggle-api/blob/main/docs/tutorials.md](https://github.com/Kaggle/kaggle-api/blob/main/docs/tutorials.md)
- **Kaggle Competitions**: [https://www.kaggle.com/competitions](https://www.kaggle.com/competitions)

## Workflow Checklist

When helping users with Kaggle API and HPCC:

- [ ] **VPN Check**: Ask about VPN connection for HPCC operations
- [ ] **Credentials Setup**: Guide through `kaggle.json` configuration
- [ ] **Installation**: Verify Kaggle API installation
- [ ] **Authentication Test**: Run `kaggle competitions list` to verify
- [ ] **HPCC Access**: Verify HPCC Jupyter access (if applicable)
- [ ] **Module Loading**: Ensure required modules loaded (HPCC)
- [ ] **Data Storage**: Guide on data location (scratch vs. home)
- [ ] **Security**: Remind about credential security

---

**Important**: Always check VPN connection first when working with HPCC resources!
