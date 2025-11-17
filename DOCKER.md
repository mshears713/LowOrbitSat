# Docker Setup for Windows

This guide will help you run ORBITER-0 on your Windows laptop using Docker.

## Prerequisites

### 1. Install Docker Desktop for Windows

Download and install Docker Desktop from: https://www.docker.com/products/docker-desktop/

**Requirements:**
- Windows 10 64-bit: Pro, Enterprise, or Education (Build 19041 or higher)
- Or Windows 11 64-bit: Home or Pro (version 21H2 or higher)
- WSL 2 feature enabled on Windows
- 4GB RAM minimum (8GB recommended)

**Installation Steps:**
1. Download Docker Desktop installer
2. Run the installer
3. Enable WSL 2 during installation (recommended)
4. Restart your computer when prompted
5. Launch Docker Desktop from Start menu
6. Wait for Docker to start (you'll see a green indicator in the system tray)

### 2. Verify Docker Installation

Open PowerShell or Command Prompt and run:

```powershell
docker --version
docker-compose --version
```

You should see version numbers for both commands.

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Open PowerShell** in the project directory:
   ```powershell
   cd path\to\LowOrbitSat
   ```

2. **Build and start the application:**
   ```powershell
   docker-compose up -d
   ```

3. **Open your browser** and navigate to:
   ```
   http://localhost:8501
   ```

4. **Stop the application:**
   ```powershell
   docker-compose down
   ```

### Option 2: Using Docker Commands Directly

1. **Build the Docker image:**
   ```powershell
   docker build -t orbiter0 .
   ```

2. **Run the container:**
   ```powershell
   docker run -d -p 8501:8501 --name orbiter0-app orbiter0
   ```

3. **Open your browser** and navigate to:
   ```
   http://localhost:8501
   ```

4. **Stop the container:**
   ```powershell
   docker stop orbiter0-app
   docker rm orbiter0-app
   ```

## Data Persistence

The SQLite database is stored in the `data/` directory on your host machine. This ensures your mission history persists even when you stop and restart containers.

To view your data directory:
```powershell
dir data
```

## Common Commands

### View running containers:
```powershell
docker ps
```

### View logs:
```powershell
# Using docker-compose
docker-compose logs -f

# Using docker directly
docker logs -f orbiter0-app
```

### Rebuild after code changes:
```powershell
# Using docker-compose
docker-compose up -d --build

# Using docker directly
docker build -t orbiter0 .
docker stop orbiter0-app
docker rm orbiter0-app
docker run -d -p 8501:8501 --name orbiter0-app orbiter0
```

### Stop and remove everything:
```powershell
docker-compose down
```

### Access container shell (for debugging):
```powershell
docker exec -it orbiter0-app /bin/bash
```

## Troubleshooting

### Port 8501 already in use

If you see an error about port 8501 being in use:

1. **Check what's using the port:**
   ```powershell
   netstat -ano | findstr :8501
   ```

2. **Stop the process or change the port** in `docker-compose.yml`:
   ```yaml
   ports:
     - "8502:8501"  # Use port 8502 instead
   ```

### Docker Desktop not starting

1. Ensure WSL 2 is enabled:
   ```powershell
   wsl --install
   ```

2. Check Docker Desktop settings:
   - Right-click Docker icon in system tray
   - Select "Settings"
   - Ensure "Use WSL 2 based engine" is checked

### Container fails to start

1. **Check logs:**
   ```powershell
   docker-compose logs
   ```

2. **Verify Docker Desktop is running** (green icon in system tray)

3. **Rebuild the image:**
   ```powershell
   docker-compose down
   docker-compose build --no-cache
   docker-compose up
   ```

### Cannot access http://localhost:8501

1. **Verify container is running:**
   ```powershell
   docker ps
   ```

2. **Check firewall settings** - ensure Docker is allowed through Windows Firewall

3. **Try 127.0.0.1 instead:**
   ```
   http://127.0.0.1:8501
   ```

### Permission issues with data directory

If you see SQLite errors:

1. **Create the data directory manually:**
   ```powershell
   mkdir data
   ```

2. **Ensure Docker Desktop has file sharing permissions:**
   - Docker Desktop Settings → Resources → File Sharing
   - Add your project directory if not listed

## Windows-Specific Notes

### File Paths
- Use backslashes (`\`) or forward slashes (`/`) in PowerShell
- Docker internally converts Windows paths automatically

### Line Endings
- If you edit files on Windows, ensure they use LF (not CRLF) line endings
- Git should handle this automatically with `.gitattributes`

### Performance
- WSL 2 provides better performance than Hyper-V
- Store project files in WSL 2 filesystem for faster builds (optional)

### Firewall
- Windows Defender may prompt to allow Docker - click "Allow"
- Corporate firewalls may block Docker - contact your IT admin

## Advanced Usage

### Custom Configuration

Edit `orbiter0/src/config/default_params.yaml` to customize simulation parameters. Changes will be reflected when you restart the container.

### Development Mode

To develop with live code reloading, mount your code as a volume:

```powershell
docker run -d -p 8501:8501 -v ${PWD}:/app --name orbiter0-app orbiter0
```

Or add to `docker-compose.yml`:
```yaml
volumes:
  - .:/app
```

### Running Self-Tests

```powershell
docker exec orbiter0-app python orbiter0/tests/self_test.py
```

## System Requirements

**Minimum:**
- 2 CPU cores
- 4GB RAM
- 2GB disk space
- Windows 10/11 with WSL 2

**Recommended:**
- 4+ CPU cores
- 8GB RAM
- 5GB disk space
- SSD storage

## Support

For issues specific to this application, check the main README.md.

For Docker Desktop issues, see: https://docs.docker.com/desktop/troubleshoot/overview/

## Next Steps

Once the application is running:
1. Open http://localhost:8501 in your browser
2. Start with "1_📡_Signals_101.py" to learn the basics
3. Progress through all 10 chapters
4. Try the "7_🛰️_Downlink_Console.py" for hands-on satellite communication
5. Review your missions in "9_📊_Mission_Archive.py"

Happy learning! 🛰️
